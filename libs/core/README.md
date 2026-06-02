# Athena Core

`athena-core` 是 Athena 项目的基础运行时工具包，提供时间解析与格式化、时区上下文、Pydantic 模型基类、带标签枚举，以及常用值处理 helper。它的定位是为 Athena 生态内的业务包提供稳定、轻量、可复用的底层能力。

## 安装

```bash
pip install athena-core
```

当前版本要求 Python 3.12 或更高版本。

## 快速开始

### 时间解析与格式化

```python
from athena_core import format_datetime, parse_datetime

dt = parse_datetime("2026-06-02 10:30:00")
text = format_datetime(dt, output_format="iso")
```

### 时区上下文

```python
from athena_core import get_timezone, timezone_context

print(get_timezone())

with timezone_context("UTC"):
    print(get_timezone())
```

默认时区为 `Asia/Shanghai`。也可以通过 `ATHENA_TIMEZONE`、`ATHENA_TZ`、`ATHENA__TIMEZONE` 或 `ATHENA__TZ` 环境变量覆盖。

### Pydantic 模型基类

```python
from athena_core import BaseAthenaModel


class User(BaseAthenaModel):
    name: str
    age: int
```

`BaseAthenaModel` 默认禁止额外字段、支持字段别名填充，并开启字符串首尾空白清理，适合在 Athena 项目中作为统一的数据模型基础。

### 值处理 helper

```python
from athena_core import first_not_none, optional_map

value = first_not_none(None, None, "fallback")
length = optional_map(value, len)
```

## 设计

`athena-core` 按能力边界组织为几个相对独立的模块：

- `athena_core.temporal`：负责日期、时间、日期时间的标准化处理，以及全局默认时区和临时时区上下文管理。
- `athena_core.temporal.codec`：提供 `parse_*` 与 `format_*` 函数，以及可复用的 codec 类。它将输入兼容、时区归一、输出格式选择收敛到统一入口。
- `athena_core.models`：提供 `BaseAthenaModel` 和带中文标签能力的枚举基类，用于减少业务包重复定义模型配置和枚举转换逻辑。
- `athena_core.values`：提供与 `None`、默认值、fallback 值相关的小型函数，保持业务代码中的空值处理表达清晰。

整体设计上，`athena-core` 不承载具体业务语义，只提供跨项目通用的基础设施。顶层 `athena_core` 会导出常用 API，子模块也保留更细粒度的导入路径，方便调用方按需选择。

## 主要 API

时间与时区：

- `parse_datetime()` / `format_datetime()`
- `parse_date()` / `format_date()`
- `parse_time()` / `format_time()`
- `timezone_context()`
- `get_timezone()` / `set_default_timezone()` / `reload_default_timezone()`
- `normalize_datetime_timezone()` / `resolve_date_boundary()`

模型与枚举：

- `BaseAthenaModel`
- `LabelIntEnum`
- `LabelStrEnum`

值处理：

- `first_not_none()`
- `first_non_empty()`
- `first_truthy()`
- `optional_map()` / `optional_map_or()` / `optional_map_or_else()`
- `optional_or()` / `optional_or_else()`
- `safe_getattr()`

## 开发

```bash
uv sync --all-packages --all-groups
uv run pytest libs/core/tests
uv run ruff check libs/core/src/athena_core libs/core/tests
uv run ruff format --check libs/core/src/athena_core libs/core/tests
```

## 构建发布包

```bash
uv build --package athena-core
```

构建产物会生成在仓库根目录的 `dist/` 目录下。发布前建议确认测试、lint、format 和构建均通过。
