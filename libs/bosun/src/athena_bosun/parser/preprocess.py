import re
from string import ascii_letters
from typing import Literal

from athena_bosun.parser.exceptions import BosunPreprocessError

type VariableStore = dict[str, str]

type AssignmentKind = Literal["variable", "alert_expression", "metadata"]


def preprocess(source: str) -> str:
    """预处理 Bosun 源文本。

    该函数用于将 Bosun 源文本转换为单个可供 Lexer 解析的表达式，支持两类输入：

    1. 查询表达式
        $start=2026-05-30 12:00
        $end=2026-05-30 13:00
        $err_kpi = "sum:1m-sum-zero:metric.error"
        $all_kpi = "sum:1m-sum-zero:metric.total"
        1 - (
            fv(nanas(q($err_kpi, "$start", "$end"), 0), 0)
            /
            (fv(nanas(q($all_kpi, "$start", "$end"), 0), 0) + 1e-16)
        )

    - `$xxx = ...` 表示变量定义
    - 非赋值语句表示查询表达式入口
    - 查询表达式入口之后不允许再出现变量定义

    2. Bosun Alert Definition

        nullAsZero = false
        $expr_0 = avg(q("sum:metric.a", "5m", "")) > 100
        $expr_1 = avg(q("sum:metric.b", "5m", "")) < 10
        warn = $expr_0 || $expr_1
        runEvery = 1

    - `$xxx = ...` 表示变量定义
    - `warn = ...` 和 `crit = ...` 表示告警表达式入口
    - `runEvery = ...` 等会被视为告警元数据，在预处理阶段忽略

    对于查询表达式和 Bosun Alert Definition，除元数据外，表达式入口应该是最后一条有效语句。

    Args:
        source: Bosun 源文本，可以是查询表达式，也可以是 Bosun Alert Definition。

    Returns:
        展开变量后的最终表达式。

    Raises:
        BosunPreprocessError: 当变量引用非法、变量未定义、表达式入口缺失，或表达式入口之后仍出现变量定义/查询表达式时抛出。
    """
    statements = _split_statements(source)
    if not statements:
        return ""

    store: VariableStore = {}
    result: str | None = None
    result_statement: str | None = None

    for statement in statements:
        expression = _decompose_statement(statement, store)
        if expression is None:  # 变量定义或元数据配置
            if result is not None and _is_variable_assignment(statement):
                raise BosunPreprocessError(f"Variable assignment cannot appear after expression entry: {statement}.")
            continue

        if result is not None:
            raise BosunPreprocessError(f"Multiple expression entries found: {result_statement}, {statement}.")

        result = expression
        result_statement = statement

    if result is None:
        raise BosunPreprocessError("Bosun source does not contain an expression entry.")
    return result


def _split_statements(source: str) -> list[str]:
    """将 Bosun 源文本拆分为语句列表。

    支持按括号层级合并多行表达式，例如：
        1 - (
            avg($a)
            /
            avg($b)
        )
    会被合并为 `1-(avg($a)/avg($b))`

    处理规则：

    1. 去除每一行首尾空白字符
    2. 忽略空行
    3. 忽略以 `#` 开头的注释行
    4. 当括号未闭合时，继续读取下一行
    5. 字符串中的括号不会影响括号层级
    """
    statements: list[str] = []
    buffer: list[str] = []

    paren_depth = 0
    in_string = False
    for line_no, raw_line in enumerate(source.splitlines(), start=1):
        line = raw_line.strip()
        if not line:  # 空行
            continue
        if line.startswith("#"):  # 注释行
            continue

        buffer.append(line)
        for ch in line:
            if ch == '"':  # 进入字符串或者退出字符串
                in_string = not in_string
                continue
            if in_string:  # 字符串中
                continue

            if ch == "(":
                paren_depth += 1
            elif ch == ")":
                paren_depth -= 1
                if paren_depth < 0:
                    raise BosunPreprocessError(f"Unexpected closing parenthesis at line {line_no}.")

        if paren_depth == 0 and not in_string:
            statements.append(" ".join(buffer))
            buffer.clear()

    if in_string:
        raise BosunPreprocessError("Unclosed string literal in Bosun source.")
    if paren_depth > 0:
        raise BosunPreprocessError("Unclosed parenthesis in Bosun source.")

    if buffer:
        statements.append(" ".join(buffer))

    return statements


def _decompose_statement(statement: str, store: VariableStore) -> str | None:
    """解析单条 Bosun 语句。

    Bosun 语句一共分为四类：

    1. 变量定义，解析变量定义并写入到变量表中，返回结果为 `None`。
        $metric = os.cpu
        $query = q("avg:$metric{host=*}", "5m", "")

    2. 查询表达式入口，展开变量后返回。
        avg($query)
        $expr_0 || $expr_1

    3. 告警表达式入口，展开变量后返回。
        warn = $expr_0 || $expr_1
        crit = avg($query) > 100

    4. 元数据配置，会被忽略并返回 `None`。
        runEvery = 1
        nullAsZero = false
        fullJoinGroup = true
    """
    assign_position = _find_top_level_assignment(statement)

    if assign_position is None:  # 查询表达式入口，展开变量后返回
        return _expand_expression(statement, store)

    name = statement[:assign_position].strip()
    value = statement[assign_position + 1 :].strip()
    if not value:
        raise BosunPreprocessError(f"Assignment value is empty: {statement}.")

    kind = _classify_assignment_name(name)
    match kind:
        case "variable":
            store[name] = _expand_expression(value, store)
            return None
        case "alert_expression":
            return _expand_expression(value, store)
        case "metadata":
            return None
        case _:
            raise BosunPreprocessError(f"Unsupported assignment kind: {kind}.")


def _find_top_level_assignment(statement: str) -> int | None:
    """查找顶层赋值符号 `=` 的位置，只识别不在字符串、不在括号内部的 `=`。

    1. `$metric = "sum:metric{host=*}"`: 会识别 `$metric = ...` 中的 `=`。
    2. `q("sum:metric{host=*}", "5m", "")`: 不会把字符串中的 `host=*` 误判为赋值语句。
    """
    paren_depth = 0
    in_string = False

    for index, ch in enumerate(statement):
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "(":
            paren_depth += 1
            continue
        if ch == ")":
            paren_depth -= 1
            continue

        if ch == "=" and paren_depth == 0:
            prev_ch = statement[index - 1] if index > 0 else ""
            next_ch = statement[index + 1] if index + 1 < len(statement) else ""
            if prev_ch in {"!", ">", "<", "="} or next_ch == "=":
                # 跳过 `==`, `!=`, `>=`, `<=`
                continue
            return index

    return None


def _classify_assignment_name(name: str) -> AssignmentKind:
    """根据赋值语句左侧名称判断赋值类型。

    - `$xxx`：变量定义
    - `warn` / `crit`：告警表达式入口
    - 判断是否为元数据配置：变量名称是否以字母开头，后接字母或数字
    - 其他：非法赋值名称
    """
    if name.startswith("$"):
        if len(name) == 1:
            raise BosunPreprocessError("Invalid variable name: '$'.")
        for index, ch in enumerate(name[1:], start=1):
            if (index == 1 and not _is_identifier_start(ch)) or (index > 1 and not _is_identifier_part(ch)):
                raise BosunPreprocessError(f"Invalid variable name: {name}")
        return "variable"

    if name in {"warn", "crit"}:
        return "alert_expression"

    if re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$").match(name):
        return "metadata"

    raise BosunPreprocessError(f"Unknown assignment name: {name!r}.")


def _is_variable_assignment(statement: str) -> bool:
    """判断语句是否为变量定义语句。"""
    assign_pos = _find_top_level_assignment(statement)
    if assign_pos is None:
        return False

    name = statement[:assign_pos].strip()
    return name.startswith("$")


def _expand_expression(expression: str, store: VariableStore) -> str:
    """展开表达式中的变量引用，所有变量都会从变量表中读取对应值并替换到表达式中。

    变量支持以下形式：
        - `$metric`
        - `${metric}`
        - `${cluster:splitByColon:0}`
    """
    parts: list[str] = []
    position = 0
    while position < len(expression):
        ch = expression[position]

        if ch != "$":
            parts.append(ch)
            position += 1
            continue

        placeholder = _extract_placeholder(expression, position)
        value = _resolve_placeholder(placeholder, store)

        parts.append(value)
        position += len(placeholder)

    return "".join(parts)


def _extract_placeholder(expression: str, position: int) -> str:
    """提取变量占位符表达式。

    - $metric
    - ${metric}
    - ${metric:splitByColon:0}
    """
    if position >= len(expression) or expression[position] != "$":
        raise BosunPreprocessError("Placeholder expression must begin with `$`.")

    if position + 1 >= len(expression):
        raise BosunPreprocessError("Invalid placeholder expression: `$`.")

    if expression[position + 1] == "{":
        return _extract_braced_placeholder(expression, position)

    return _extract_simple_placeholder(expression, position)


def _extract_simple_placeholder(expression: str, position: int) -> str:
    """提取简单变量占位符。

    Examples:
        `$metric`
    """
    start = position
    end = start + 1

    while end < len(expression):
        ch = expression[end]
        if _is_identifier_part(ch):
            end += 1
        else:
            break

    placeholder = expression[start:end]
    if len(placeholder) <= 1 or not _is_identifier_start(placeholder[1]):
        raise BosunPreprocessError(f"Invalid placeholder expression: {placeholder}.")

    return placeholder


def _extract_braced_placeholder(expression: str, position: int) -> str:
    """提取花括号形式的变量占位符。

    Examples:
        `${metric}`
        `${api:splitByColon:1}`
    """
    start = position
    end = start + 2

    while end < len(expression):
        ch = expression[end]
        if ch == "}":
            placeholder = expression[start : end + 1]
            if placeholder == r"${}":
                raise BosunPreprocessError(r"Invalid placeholder expression: ${}.")
            if not _is_identifier_start(placeholder[2]):  # ${? → `?`必须是合法的变量起始字符
                raise BosunPreprocessError(f"Invalid placeholder expression: {placeholder}.")
            return placeholder

        if _is_identifier_part(ch) or ch == ":":
            end += 1
            continue

        raise BosunPreprocessError(f"Invalid character {ch} in placeholder expression.")

    raise BosunPreprocessError(f"Unclosed placeholder expression: {expression[start:]}")


def _resolve_placeholder(placeholder_expr: str, store: VariableStore) -> str:
    """解析并计算变量占位符。

    1. 普通变量引用，例如 `$metric`, `${metric}`。
    2. splitByColon 函数: `${api:splitByColon:0}`。
    """
    inner = placeholder_expr[2:-1] if placeholder_expr.startswith("${") else placeholder_expr[1:]

    parts = inner.split(":")
    if len(parts) not in {1, 3}:
        raise BosunPreprocessError(f"Invalid placeholder expression: {placeholder_expr}.")

    name = f"${parts[0]}"  # variable name
    origin_value = store.get(name)
    if origin_value is None:
        raise BosunPreprocessError(f"Placeholder {name} is not defined.")

    if len(parts) == 1:  # $metric, ${metric}
        return origin_value

    # ${api:splitByColon:0}
    func_name = parts[1]
    arg = parts[2]
    if func_name != "splitByColon":
        raise BosunPreprocessError(f"Placeholder function {func_name} is not implemented.")
    try:
        index = int(arg)
    except ValueError as exc:
        raise BosunPreprocessError(f"Placeholder index must be an integer: {arg}.") from exc

    values = origin_value.split(":")
    if index < 0 or index >= len(values):
        raise BosunPreprocessError(f"Placeholder value {origin_value} does not have index={index}.")

    return values[index]


def _is_identifier_start(ch: str) -> bool:
    """判断字符是否可以作为标识符首字符。"""
    return ch == "_" or ch in ascii_letters


def _is_identifier_part(ch: str) -> bool:
    """判断字符是否可以作为标识符组成字符。"""
    return _is_identifier_start(ch) or ch.isdigit()
