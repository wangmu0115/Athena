from __future__ import annotations


def extract_query(expr: Expression, queries: list[Query]):
    match expr:
        case NameExpression() | LiteralExpression():
            ...
        case UnaryOperatorExpression():
            extract_query(expr.right, queries)
        case BinaryOperatorExpression():
            extract_query(expr.left, queries)
            extract_query(expr.right, queries)
        case CallExpression():
            match expr.function:
                case "q":  # q(query_string, start, end)
                    queries.append(Query.strpquery(expr.args[0].literal))
                case "shift" | "sum" | "avg" | "max" | "min" | "fv" | "nv" | "nanas":
                    extract_query(expr.args[0], queries)
                case _:
                    raise NotImplementedError(f"[Extract Expr Queries] Not implemented call function: {expr.function}")
        case _:
            raise NotImplementedError(f"[Extract Expr Queries] Not implemented expression: {expr}")


def extract_queries_formula(expr: Expression, named_queries: dict[str, Query]) -> str:
    match expr:
        case NameExpression():
            return expr.name
        case LiteralExpression():
            return expr.literal
        case UnaryOperatorExpression():
            right = extract_queries_formula(expr.right, named_queries)
            return f"({expr.operator.text}{right})"
        case BinaryOperatorExpression():
            left = extract_queries_formula(expr.left, named_queries)
            right = extract_queries_formula(expr.right, named_queries)
            return f"({left}{expr.operator.text}{right})"
        case CallExpression():
            match expr.function:
                case "q":
                    query = Query.strpquery(expr.args[0].literal)
                    for name, namedquery in named_queries.items():
                        if query == namedquery:
                            return name
                case "shift" | "sum" | "avg" | "max" | "min" | "fv" | "nv" | "nanas":
                    return extract_queries_formula(expr.args[0], named_queries)
                case _:
                    raise NotImplementedError(f"[Extract Expr Queries Formula] Not implemented call function: {expr.function}")
        case _:
            raise NotImplementedError(f"[Extract Expr Queries Formula] Not implemented expression: {expr}")


class Program:
    def __init__(self, expression: Expression):
        self.expression = expression

    def extract_all_queries(self) -> list[Query]:
        queries = []
        extract_query(self.expression, queries)
        distincted_queries = []
        for query in queries:
            if query not in distincted_queries:
                distincted_queries.append(query)
        return distincted_queries

    def extract_calc_formula(self):
        named_queries = {f"$kpi{index}": query for index, query in enumerate(self.extract_all_queries())}
        formula = extract_queries_formula(self.expression, named_queries)

        return f"{'\n\n'.join(f'{name}={str(query)}' for name, query in named_queries.items())}\n\n{formula}"

    def pprint(self):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}(expression={self.expression!r})"


class Expression:
    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(f'{attr_name}={attr_value!r}' for attr_name, attr_value in self.__dict__.items())})"


class NameExpression(Expression):  # 名称表达式
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name


LiteralType = TypeVar("LiteralType", int, float, str)


class LiteralExpression(Expression, Generic[LiteralType]):
    def __init__(self, literal: LiteralType):
        self.literal = literal

    def __str__(self):
        return str(self.literal)


class IntLiteralExpression(LiteralExpression[int]): ...


class FloatLiteralExpression(LiteralExpression[float]): ...


class StrLiteralExpression(LiteralExpression[str]):
    def __str__(self):
        return f'"{self.literal}"'


class UnaryOperatorExpression(Expression):
    def __init__(self, operator: Token, right: Expression):
        self.operator = operator
        self.right = right

    def __str__(self):
        return f"({self.operator.text}{str(self.right)})"


class BinaryOperatorExpression(Expression):
    def __init__(self, left: Expression, operator: Token, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        return f"({str(self.left)} {self.operator.text} {str(self.right)})"


class CallExpression(Expression):
    def __init__(self, function: str, args: list[Expression]):
        self.function = function
        self.args = args

    def __str__(self):
        return f"{self.function}({','.join(str(arg) for arg in self.args)})"
