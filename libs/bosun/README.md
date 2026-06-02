# athena-bosun

`athena-bosun` 是 Athena 项目中的 Bosun 表达式工具包，提供 Bosun 源文本预处理、表达式解析、AST 分析，以及 OpenTSDB 查询字符串的解析和序列化能力。

它主要覆盖三类工作流：

- 将 Bosun 风格的变量定义和告警文本展开为可解析的表达式。
- 将表达式解析为轻量、不可变的 AST。
- 解析、构造、规范化和渲染 OpenTSDB 查询字符串。

## 安装

该包要求 Python 3.12 或更高版本。

```bash
pip install athena-bosun
```

在 Athena workspace 中，可以使用 uv 安装或运行：

```bash
uv sync --package athena-bosun
```

## 快速开始

预处理 Bosun 源文本，解析为 AST，并提取 OpenTSDB 查询：

```python
from athena_bosun import Lexer, Parser, preprocess
from athena_bosun.ast import extract_all_queries, render_calc_formula

source = """
$metric = "sum:service.qps"
$query = q($metric, "5m", "")

avg($query) > 100
"""

expression = preprocess(source)
program = Parser(Lexer(expression, preprocessed=True)).parse()

queries = extract_all_queries(program)
formula = render_calc_formula(program)

print(expression)
print(queries)
print(formula)
```

直接解析 OpenTSDB 查询字符串：

```python
from athena_bosun.opentsdb import parse_query

query = parse_query(
    "sum:1m-avg:rate{counter,,,diff,after_downsample}:"
    "[tenant]service.latency{host=a|b}{env=prod}[rt.pct90,count.rate]"
)

print(query.metric)
print(query.to_query_string())
```

使用结构化模型构造查询：

```python
from athena_bosun.opentsdb import Aggregator, Downsampling, Query, Rate, TagKv

query = Query(
    aggregator=Aggregator.SUM,
    downsampling=Downsampling(interval="1m", aggregator=Aggregator.AVG),
    rate=Rate(counter=True, delta=False),
    metric="service.qps",
    groups=[TagKv(key="host", values=["a", "b"], group_by=True)],
)

print(query.to_query_string())
```

## 设计思路

`athena-bosun` 按职责拆成四层，尽量让每一层只处理一种问题。

### 预处理层

`preprocess()` 负责把 Bosun 源文本转换成单个表达式。它会处理变量定义、变量引用、`${name:splitByColon:index}` 这类占位符、`warn` / `crit` 告警入口，以及 `runEvery` 等元数据。

这一层不关心表达式语法是否正确，也不构造 AST；它只负责把输入文本整理成后续 Lexer 可以处理的一段表达式。

### 词法和语法解析层

`Lexer` 将预处理后的表达式拆成 `Token` 序列。`Parser` 使用 Pratt parsing 构建表达式 AST，`parselets.py` 中的 parselet 定义了前缀表达式、二元运算、括号分组和函数调用的解析规则。

`parser.py` 和 `parselets.py` 放在 parser 层是刻意的：

- `parser.py` 维护 Pratt parser 的解析状态。
- `parselets.py` 描述不同 token 对应的解析规则。
- `tokens.py` 和 `lexer.py` 保持词法职责。

这种拆分让新增运算符或函数调用语法时，可以优先扩展 parselet，而不需要重写整个 parser。

### AST 层

`athena_bosun.ast.nodes` 只定义纯 AST 节点，例如 `Program`、`BinaryOperatorExpression`、`CallExpression`。这些节点不依赖 OpenTSDB，也不包含 query 提取等业务逻辑。

`athena_bosun.ast.queries` 负责基于 AST 做业务分析：

- `extract_all_queries(program)` 从表达式中提取所有 `q(...)` 调用里的 OpenTSDB 查询，并按首次出现顺序去重。
- `render_calc_formula(program)` 将 `q(...)` 替换为 `$kpiN`，并生成 `$kpiN=query` 定义和最终公式。

这样可以保持 AST 节点层干净，也让后续增加新的 AST 分析能力更自然。

### OpenTSDB 层

`athena_bosun.opentsdb` 负责 OpenTSDB 查询字符串和结构化模型之间的转换：

- `parser.py`：字符串到模型，例如 `parse_query()`。
- `serializer.py`：模型到字符串，例如 `serialize_query()`。
- `models.py`：结构化模型，例如 `Query`、`Downsampling`、`TagKv`。
- `enums.py`：聚合方式、过滤函数、多值字段函数等枚举。
- `intervals.py`：interval 字符串换算等辅助能力。

这一层和 Bosun 表达式 parser 相互独立。AST 分析阶段只在遇到 `q(...)` 时调用 OpenTSDB parser，把查询字符串解析成 `Query`。

## 公开 API

顶层包：

- `preprocess(source)`：将 Bosun 源文本转换为单个表达式。
- `Lexer(expression, preprocessed=True)`：将表达式转换为 token 序列。
- `Parser(lexer).parse()`：解析表达式并返回 AST `Program`。

AST helpers：

- `extract_all_queries(program)`：按首次出现顺序返回唯一 OpenTSDB `Query` 列表。
- `render_calc_formula(program)`：渲染 `$kpiN=query` 定义和引用这些名称的计算公式。

OpenTSDB helpers：

- `parse_query()`、`parse_downsampling()`、`parse_rate()`、`parse_topk()`、`parse_tagkv()`、`parse_multifield()`
- `serialize_query()`、`serialize_downsampling()`、`serialize_rate()`、`serialize_topk()`、`serialize_tagkv()`、`serialize_multifield()`
- 模型：`Query`、`Downsampling`、`Rate`、`TopK`、`TagKv`、`MultiField`
- 枚举：`Aggregator`、`FilterType`、`MultiFunction`

## 示例

Athena 仓库的 `examples/bosun` 目录中提供了可运行示例：

- `opentsdb_parse_query.py`
- `opentsdb_build_query.py`
- `preprocess_and_parse.py`
- `render_calc_formula.py`

从 workspace 根目录运行示例：

```bash
PYTHONPATH=libs/bosun/src:libs/core/src python examples/bosun/preprocess_and_parse.py
```

## 开发

运行测试：

```bash
PYTHONPATH=libs/bosun/src:libs/core/src pytest libs/bosun/tests
```

运行 lint 和格式检查：

```bash
ruff check libs/bosun/src/athena_bosun libs/bosun/tests examples/bosun
ruff format --check libs/bosun/src/athena_bosun libs/bosun/tests examples/bosun
```

构建发布包：

```bash
uv build --package athena-bosun
```
