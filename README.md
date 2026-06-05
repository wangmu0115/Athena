# Athena Kit

Athena Kit is a modular Python toolkit for Athena projects.

It ships one distribution package, `athena-kit`, and exposes one Python
namespace, `athena_kit`.

## Installation

```shell
uv add athena-kit
uv add "athena-kit[http]"
uv add "athena-kit[matplotlib]"
uv add "athena-kit[dataframe]"
uv add "athena-kit[all]"
```

## Usage

```python
from athena_kit.core import format_datetime, parse_datetime
from athena_kit.http import AsyncHttpClient
from athena_kit.bosun import Lexer, Parser
```

Matplotlib utilities are available when the `matplotlib` extra is installed:

```python
from athena_kit.matplotlib.runtime.pipeline import Pipeline
```

## Layout

- `athena_kit.core`: base models, temporal codecs, tabular helpers, and value helpers.
- `athena_kit.http`: thin async HTTP client utilities built on `httpx`.
- `athena_kit.matplotlib`: declarative chart rendering utilities.
- `athena_kit.bosun`: Bosun expression parsing and OpenTSDB query utilities.

## Development

```shell
uv sync --extra all
uv run ruff check src tests examples
uv run ruff format --check src tests examples
uv run pytest tests
```
