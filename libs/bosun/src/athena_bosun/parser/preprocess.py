import re
from string import ascii_letters
from typing import Literal

from athena_bosun.parser.exceptions import BosunPreprocessError

type VariableStore = dict[str, str]

type AssignmentKind = Literal["variable", "alert_expression", "metadata"]

_ALERT_EXPRESSION_KEYS = {"warn", "crit"}

_METADATA_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def preprocess(source: str) -> str:
    """预处理 Bosun 源文本。

    该函数用于将 Bosun 源文本转换为单个可供 Lexer 解析的表达式，支持两类输入：

    1. 查询表达式

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

        if result is not None:
            raise BosunPreprocessError(f"Only the last statement can be an expression: {statement}.")

    result = _decompose_statement(statements[-1], store)
    if result is None:
        raise BosunPreprocessError("The last statement must be a query expression.")

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
    escaped = False
    for line_no, raw_line in enumerate(source.splitlines(), start=1):
        line = raw_line.strip()
        if not line:  # 空行
            continue
        if line.startswith("#"):  # 注释行
            continue

        buffer.append(line)

        for ch in line:
            if ch == "\\" and in_string:  # 字符串中的转义字符
                escaped = True
                continue
            if escaped:  # \ 后面的字符是转义字符
                escaped = False
                continue
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

    Bosun 语句分为三类：

    1. variable
        `$xxx = ...` 形式的变量定义语句。

    2. expression


    支持两种语句形式：

        1. 变量定义: `$metric = os.cpu`，会将展开后的结果写入变量表。
        2. 查询表达式: `avg($metric)`，会返回展开后的表达式内容。

    Args:
        statement: 单条 Bosun 语句。
        store: 变量存储表。

    Returns:
        - 变量定义语句返回 None
        - 表达式语句返回展开后的表达式
    """
    lhs, sep, rhs = statement.partition("=")
    if sep != "=":
        return _expand_expression(statement, store)

    kind = _classify_assignment_lhs(lhs)

    if kind == "variable":
        name = lhs.strip()
        store[name] = _expand_expression(rhs.strip(), store)
        return None

    if kind == "alert_expression":
        return _expand_expression(rhs.strip(), store)

    return None


def _classify_assignment_lhs(lhs: str) -> AssignmentKind:
    """根据赋值语句左侧内容判断赋值类型。

    判断规则：

    - `$xxx`：变量定义
    - `warn` / `crit`：告警表达式入口
    - 其他名称：元数据配置

    Args:
        lhs:
            赋值语句左侧文本。

    Returns:
        赋值类型。
    """
    name = lhs.strip()

    if name.startswith("$"):
        return "variable"

    if name in _ALERT_EXPRESSION_KEYS:
        return "alert_expression"

    return "metadata"


def _is_variable_assignment(statement: str) -> bool:
    """判断语句是否为变量定义语句。"""
    lhs, sep, _ = statement.partition("=")
    return sep == "=" and lhs.strip().startswith("$")


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
    if len(placeholder) <= 1:
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
            return expression[start : end + 1]

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
