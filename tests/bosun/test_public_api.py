import athena_kit.bosun
from athena_kit.bosun import Lexer, Parser, preprocess
from athena_kit.bosun.ast import extract_all_queries, render_calc_formula
from athena_kit.bosun.opentsdb import Query, parse_query


def test_top_level_api_exports_parser_and_preprocess():
    expression = preprocess('$metric = "sum:service.qps"\nq($metric, "5m", "")')
    program = Parser(Lexer(expression, preprocessed=True)).parse()

    assert athena_kit.bosun.Lexer is Lexer
    assert athena_kit.bosun.Parser is Parser
    assert expression == 'q("sum:service.qps", "5m", "")'
    assert [str(query) for query in extract_all_queries(program)] == ["sum:[default]service.qps{}{}"]
    assert render_calc_formula(program) == "$kpi0=sum:[default]service.qps{}{}\n\n$kpi0"


def test_opentsdb_package_exports_parse_query():
    query = parse_query("sum:service.qps")

    assert isinstance(query, Query)
    assert str(query) == "sum:[default]service.qps{}{}"
