from typing import Literal

type AxisDataType = Literal["timestamp_ms", "timestamp_s", "datetime", "date", "time", "number", "category"]
"""坐标轴数据类型定义，用于描述坐标轴数据的语义类型。

取值说明：
    - timestamp_ms: 毫秒级 Unix 时间戳。
    - timestamp_s: 秒级 Unix 时间戳。
    - datetime: 日期时间类型，通常对应 `datetime` 对象或日期时间字符串。
    - date: 日期类型，通常对应 `date` 对象或日期字符串。
    - time: 时间类型，通常对应 `time` 对象或时间字符串。
    - number: 连续数值类型。
    - category: 离散分类类型。

该类型通常用于坐标轴数据归一化、刻度格式化、坐标系适配和渲染引擎中的轴类型判断。
"""


type TickFormatterKind = Literal["auto", "datetime", "date", "time", "number", "category", "percent", "currency"]
"""刻度标签格式化类型定义，用于描述坐标轴刻度标签的显示格式。

取值说明：
    - auto: 根据 `AxisDataType` 自动推断格式化方式。自动推断规则：
        - `timestamp_ms` → `datetime`
        - `timestamp_s` → `datetime`
        - `datetime` → `datetime`
        - `date` → `date`
        - `time` → `time`
        - `number` → `number`
        - `category` → `category`
    - datetime: 日期时间格式化，通常对应完整日期时间展示，例如 `2026-01-01 12:00:00`、`01-01 12:00` 等。
    - date: 日期格式化，通常只展示日期部分，例如 `2026-01-01`、`01-01` 等。
    - time: 时间格式化，通常只展示时间部分，例如 `12:00:00`、`12:00` 等。
    - number: 数值格式化，通常用于普通数值、指标值、连续坐标轴等，例如 `1234.567 → 1234.57`、`0.1234 → 0.12` 等。
    - category: 分类文本格式化，通常直接转换为字符串展示，例如 `Q1`、`Q2`、`北京`、`男` 等。
    - percent: 百分比格式化，输入值通常为 `0 ~ 1` 的浮点数，例如 `0.123 → 12.3%`、`1.0 → 100%` 等。
    - currency: 货币格式化，通常用于金额、GMV、收入等指标，例如 `1234.56 → $1,234.56`、`1000000 → ¥1,000,000.00` 等。

该类型只影响“刻度标签显示文本”，不会影响坐标轴底层数据类型。例如：`AxisDataType="datetime"` 表示底层坐标值是日期时间，
`TickFormatterKind="time"` 表示刻度标签仅显示时间部分。
"""
