from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_bosun.ast.nodes import (
        BinaryOperatorExpression,
        CallExpression,
        Expression,
        FloatLiteralExpression,
        IntLiteralExpression,
        LiteralExpression,
        LiteralValue,
        NameExpression,
        Program,
        StrLiteralExpression,
        UnaryOperatorExpression,
    )
    from athena_bosun.ast.queries import (
        extract_all_queries,
        extract_query,
        render_calc_formula,
        render_expression_formula,
    )

__all__ = (
    "BinaryOperatorExpression",
    "CallExpression",
    "Expression",
    "FloatLiteralExpression",
    "IntLiteralExpression",
    "LiteralExpression",
    "LiteralValue",
    "NameExpression",
    "Program",
    "StrLiteralExpression",
    "UnaryOperatorExpression",
    "extract_all_queries",
    "extract_query",
    "render_calc_formula",
    "render_expression_formula",
)

_dynamic_imports = {
    "BinaryOperatorExpression": "nodes",
    "CallExpression": "nodes",
    "Expression": "nodes",
    "FloatLiteralExpression": "nodes",
    "IntLiteralExpression": "nodes",
    "LiteralExpression": "nodes",
    "LiteralValue": "nodes",
    "NameExpression": "nodes",
    "Program": "nodes",
    "StrLiteralExpression": "nodes",
    "UnaryOperatorExpression": "nodes",
    "extract_all_queries": "queries",
    "extract_query": "queries",
    "render_calc_formula": "queries",
    "render_expression_formula": "queries",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
