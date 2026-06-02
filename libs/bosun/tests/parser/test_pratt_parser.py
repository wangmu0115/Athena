from athena_bosun.ast.ast import BinaryOperatorExpression, CallExpression, Program
from athena_bosun.parser import Lexer, Parser, TokenType


def parse_expression(source: str) -> Program:
    return Parser(Lexer(source, preprocessed=True)).parse()


def test_parser_preserves_operator_precedence():
    program = parse_expression("1 + 2 * 3")

    assert isinstance(program.expression, BinaryOperatorExpression)
    assert program.expression.operator.type == TokenType.ADD
    assert isinstance(program.expression.right, BinaryOperatorExpression)
    assert program.expression.right.operator.type == TokenType.MUL
    assert str(program.expression) == "(1 + (2 * 3))"


def test_parser_parses_grouped_expression():
    program = parse_expression("(1 + 2) * 3")

    assert isinstance(program.expression, BinaryOperatorExpression)
    assert program.expression.operator.type == TokenType.MUL
    assert isinstance(program.expression.left, BinaryOperatorExpression)
    assert program.expression.left.operator.type == TokenType.ADD
    assert str(program.expression) == "((1 + 2) * 3)"


def test_parser_parses_call_expression():
    program = parse_expression('nv(q("sum:service.qps", "5m", ""), 0)')

    assert isinstance(program.expression, CallExpression)
    assert program.expression.function == "nv"
    assert len(program.expression.args) == 2
    assert isinstance(program.expression.args[0], CallExpression)
    assert program.expression.args[0].function == "q"


def test_program_extract_all_queries_deduplicates_queries():
    program = parse_expression(
        'q("sum:service.qps", "5m", "") + nv(q("sum:service.qps", "5m", ""), 0) + q("avg:service.qps", "5m", "")'
    )

    queries = program.extract_all_queries()

    assert [str(query) for query in queries] == [
        "sum:[default]service.qps{}{}",
        "avg:[default]service.qps{}{}",
    ]


def test_program_extract_calc_formula_replaces_queries_with_names():
    program = parse_expression('q("sum:service.qps", "5m", "") + avg(q("avg:service.qps", "5m", ""))')

    assert program.extract_calc_formula() == (
        "$kpi0=sum:[default]service.qps{}{}\n\n$kpi1=avg:[default]service.qps{}{}\n\n($kpi0+$kpi1)"
    )
