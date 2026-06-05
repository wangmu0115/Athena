from athena_kit.bosun import Lexer, Parser, preprocess
from athena_kit.bosun.ast import extract_all_queries

source = """
$metric = "sum:service.qps"
$query = q($metric, "5m", "")

avg($query) > 100
"""

expression = preprocess(source)
program = Parser(Lexer(expression, preprocessed=True)).parse()
queries = extract_all_queries(program)

print(expression)
print(program)
print(queries)
