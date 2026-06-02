from __future__ import annotations

from dataclasses import dataclass

from athena_bosun.opentsdb import Query
from athena_bosun.parser.tokens import Token

type LiteralValue = int | float | str


def extract_query(expr: Expression, queries: list[Query]) -> None:
    """从表达式树中收集所有 `q(...)` 调用里的 OpenTSDB 查询。"""
    match expr:
        case NameExpression() | LiteralExpression():
            return
        case UnaryOperatorExpression(right=right):
            extract_query(right, queries)
        case BinaryOperatorExpression(left=left, right=right):
            extract_query(left, queries)
            extract_query(right, queries)
        case CallExpression(function="q", args=args):
            queries.append(Query.parse_query(_require_string_literal(args, "q")))
        case CallExpression(function=function, args=args) if function in _QUERY_WRAPPER_FUNCTIONS:
            extract_query(args[0], queries)
        case CallExpression(function=function):
            raise NotImplementedError(f"[Extract Expr Queries] Not implemented call function: {function}")
        case _:
            raise NotImplementedError(f"[Extract Expr Queries] Not implemented expression: {expr}")


def extract_queries_formula(expr: Expression, named_queries: dict[str, Query]) -> str:
    """将表达式树中的 `q(...)` 调用替换为命名查询变量。"""
    match expr:
        case NameExpression(name=name):
            return name
        case LiteralExpression(literal=literal):
            return str(literal)
        case UnaryOperatorExpression(operator=operator, right=right):
            return f"({operator.text}{extract_queries_formula(right, named_queries)})"
        case BinaryOperatorExpression(left=left, operator=operator, right=right):
            left_formula = extract_queries_formula(left, named_queries)
            right_formula = extract_queries_formula(right, named_queries)
            return f"({left_formula}{operator.text}{right_formula})"
        case CallExpression(function="q", args=args):
            query = Query.parse_query(_require_string_literal(args, "q"))
            for name, named_query in named_queries.items():
                if query == named_query:
                    return name
            raise ValueError(f"Query is not registered in named_queries: {query}")
        case CallExpression(function=function, args=args) if function in _QUERY_WRAPPER_FUNCTIONS:
            return extract_queries_formula(args[0], named_queries)
        case CallExpression(function=function):
            raise NotImplementedError(f"[Extract Expr Queries Formula] Not implemented call function: {function}")
        case _:
            raise NotImplementedError(f"[Extract Expr Queries Formula] Not implemented expression: {expr}")


@dataclass(frozen=True, slots=True)
class Program:
    """Bosun 表达式 AST 根节点。"""

    expression: Expression

    def extract_all_queries(self) -> list[Query]:
        """提取表达式中出现的查询，并按首次出现顺序去重。"""
        queries: list[Query] = []
        extract_query(self.expression, queries)

        distinct_queries: list[Query] = []
        for query in queries:
            if query not in distinct_queries:
                distinct_queries.append(query)
        return distinct_queries

    def extract_calc_formula(self) -> str:
        """生成命名查询定义和替换后的计算公式。"""
        named_queries = {f"$kpi{index}": query for index, query in enumerate(self.extract_all_queries())}
        formula = extract_queries_formula(self.expression, named_queries)
        query_definitions = "\n\n".join(f"{name}={query}" for name, query in named_queries.items())
        return f"{query_definitions}\n\n{formula}"


class Expression:
    """Bosun 表达式 AST 节点基类。"""


@dataclass(frozen=True, slots=True)
class NameExpression(Expression):
    """名称表达式，例如函数名或变量名。"""

    name: str

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True, slots=True)
class LiteralExpression(Expression):
    """字面量表达式。"""

    literal: LiteralValue

    def __str__(self) -> str:
        return str(self.literal)


class IntLiteralExpression(LiteralExpression): ...


class FloatLiteralExpression(LiteralExpression): ...


class StrLiteralExpression(LiteralExpression):
    """字符串字面量表达式。"""

    literal: str

    def __str__(self) -> str:
        return f'"{self.literal}"'


@dataclass(frozen=True, slots=True)
class UnaryOperatorExpression(Expression):
    """一元运算表达式。"""

    operator: Token
    right: Expression

    def __str__(self) -> str:
        return f"({self.operator.text}{self.right})"


@dataclass(frozen=True, slots=True)
class BinaryOperatorExpression(Expression):
    """二元运算表达式。"""

    left: Expression
    operator: Token
    right: Expression

    def __str__(self) -> str:
        return f"({self.left} {self.operator.text} {self.right})"


@dataclass(frozen=True, slots=True)
class CallExpression(Expression):
    """函数调用表达式。"""

    function: str
    args: list[Expression]

    def __str__(self) -> str:
        return f"{self.function}({','.join(str(arg) for arg in self.args)})"


_QUERY_WRAPPER_FUNCTIONS = frozenset({"shift", "sum", "avg", "max", "min", "fv", "nv", "nanas"})


def _require_string_literal(args: list[Expression], function: str) -> str:
    if not args or not isinstance(args[0], StrLiteralExpression):
        raise ValueError(f"`{function}` first argument must be a string literal.")
    return args[0].literal
