from athena_kit.bosun import Lexer, Parser
from athena_kit.bosun.ast import render_calc_formula

expression = 'q("sum:service.qps", "5m", "") + avg(q("avg:service.latency", "5m", ""))'
program = Parser(Lexer(expression, preprocessed=True)).parse()

print(render_calc_formula(program))
