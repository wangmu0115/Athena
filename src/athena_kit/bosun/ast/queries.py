from athena_kit.bosun.ast.nodes import (
    BinaryOperatorExpression,
    CallExpression,
    Expression,
    LiteralExpression,
    NameExpression,
    Program,
    StrLiteralExpression,
    UnaryOperatorExpression,
)
from athena_kit.bosun.opentsdb import Query, parse_query

_QUERY_WRAPPER_FUNCTIONS = frozenset({
    "shift",
    "sum",
    "avg",
    "max",
    "min",
    "fv",
    "nv",
    "nanas",
})


def extract_query(expr: Expression, queries: list[Query]) -> None:
    """从表达式树中收集所有 `q(...)` 调用中的 OpenTSDB `Query`。

    该函数会递归遍历表达式树，并把每个 `q(query_string, start, end)`
    的第一个字符串参数解析为 `Query` 后追加到 `queries`。
    `sum`、`avg`、`shift`、`nv` 等包装函数会继续向第一个参数内部递归，暂不支持的函数会抛出 `NotImplementedError`。
    """
    match expr:
        case NameExpression() | LiteralExpression():
            return

        case UnaryOperatorExpression(right=right):
            extract_query(right, queries)

        case BinaryOperatorExpression(left=left, right=right):
            extract_query(left, queries)
            extract_query(right, queries)

        case CallExpression(function="q", args=args):
            queries.append(parse_query(_require_string_literal(args, "q")))
        case CallExpression(function=function, args=args) if function in _QUERY_WRAPPER_FUNCTIONS:
            extract_query(args[0], queries)
        case CallExpression(function=function):
            raise NotImplementedError(f"[Extract Expr Queries] Not implemented call function: {function}.")

        case _:
            raise NotImplementedError(f"[Extract Expr Queries] Not implemented expression: {expr}.")


def extract_all_queries(program: Program) -> list[Query]:
    """提取程序中出现的 OpenTSDB `Query`，并按首次出现顺序去重。

    `Query` 的相等性由 `athena_kit.bosun.opentsdb.models.Query.__eq__` 决定，同一个查询即使出现在多个位置，
    也只会保留第一次出现的实例。返回顺序用于后续生成 `$kpi0`、`$kpi1` 等稳定命名。
    """
    queries: list[Query] = []
    extract_query(program.expression, queries)

    distinct_queries: list[Query] = []
    for query in queries:
        if query not in distinct_queries:
            distinct_queries.append(query)

    return distinct_queries


def render_expression_formula(expr: Expression, named_queries: dict[str, Query]) -> str:
    """将表达式树中的 `q(...)` 调用替换为命名查询变量。

    - `named_queries` 是变量名到 `Query` 的映射，例如 `{"$kpi0": query}`。
    - 遍历过程中遇到 `q(...)` 时，会解析其查询字符串并查找等价 `Query`，然后返回对应变量名。
    - 普通运算表达式会保留括号结构，包装函数会继续向第一个参数内部递归。
    """
    match expr:
        case NameExpression(name=name):
            return name

        case LiteralExpression(literal=literal):
            return str(literal)

        case UnaryOperatorExpression(operator=operator, right=right):
            return f"({operator.text}{render_expression_formula(right, named_queries)})"

        case BinaryOperatorExpression(left=left, operator=operator, right=right):
            left_formula = render_expression_formula(left, named_queries)
            right_formula = render_expression_formula(right, named_queries)
            return f"({left_formula}{operator.text}{right_formula})"

        case CallExpression(function="q", args=args):
            query: Query = parse_query(_require_string_literal(args, "q"))
            for name, named_query in named_queries.items():
                if query == named_query:
                    return name
            raise ValueError(f"Query is not registered in named_queries: {query}.")
        case CallExpression(function=function, args=args) if function in _QUERY_WRAPPER_FUNCTIONS:
            return render_expression_formula(args[0], named_queries)
        case CallExpression(function=function):
            raise NotImplementedError(f"[Extract Expr Queries Formula] Not implemented call function: {function}.")

        case _:
            raise NotImplementedError(f"[Extract Expr Queries Formula] Not implemented expression: {expr}.")


def render_calc_formula(program: Program) -> str:
    """生成命名查询定义和替换后的计算公式。

    输出由两部分组成：

    - 前半部分是 `$kpiN=query` 的查询定义列表。
    - 后半部分是把原始表达式中的 `q(...)` 替换为 `$kpiN` 后的计算公式。

    两部分之间使用空行分隔，便于直接展示或写入 Bosun 风格文本。
    """
    named_queries = {f"$kpi{index}": query for index, query in enumerate(extract_all_queries(program))}
    formula = render_expression_formula(program.expression, named_queries)

    query_definitions = "\n\n".join(f"{name}={query}" for name, query in named_queries.items())

    return f"{query_definitions}\n\n{formula}"


def _require_string_literal(args: list[Expression], function: str) -> str:
    if not args or not isinstance(args[0], StrLiteralExpression):
        raise ValueError(f"`{function}` first argument must be a string literal.")

    return args[0].literal
