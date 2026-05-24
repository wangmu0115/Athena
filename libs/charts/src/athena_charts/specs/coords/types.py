from typing import Literal

type CoordKind = Literal["cartesian", "polar"]
"""坐标系类型定义，用于描述图表所使用的坐标系类型。

取值说明：
    - cartesian: 笛卡尔直角坐标系，使用相互垂直的 X/Y 坐标轴描述数据位置，是最常见的二维图表坐标系。
    - polar: 极坐标系，使用“角度 + 半径”描述数据位置。

坐标系类型决定了：
    - 图表允许使用的 plot 类型，例如 `LinePlot` 只能绘制在 `cartesian` 中。
    - 坐标轴结构。
    - 刻度布局方式。
    - 数据映射规则。
    - 渲染引擎中的绘制逻辑。
"""


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


type AxisScale = Literal["linear", "log"]
"""坐标轴缩放类型定义，用于描述坐标轴的数据映射方式。

取值说明：
    - linear: 线性缩放，坐标轴上的数值按照线性比例映射到屏幕坐标。
        这是最常见的坐标轴缩放方式，适用于：普通数值轴、时间轴、分类轴以及大多数统计图表等。
    - log: 对数缩放，坐标轴上的数值按照对数比例映射到屏幕坐标。
        适用于：数值跨度非常大的数据、指数增长数据、科学计量数据以及指标数量级差异较大的场景等。
        对数坐标轴通常只支持正数，`0` 和负数通常无法在对数坐标系中显示。

该类型只描述数据到坐标空间的数学映射方式，

相关概念：
    - `AxisDataType` 描述坐标轴数据语义类型。
    - `TickLocator` 描述刻度位置如何生成。
    - `TickLabelFormat` 描述刻度标签如何显示。
"""


type CartesianAxisPosition = Literal["bottom", "top", "left", "right"]
"""笛卡尔坐标轴位置定义，用于描述坐标轴在图表中的布局位置。

取值说明：
    - bottom: 底部 X 轴，通常作为默认主 X 轴，刻度标签显示在图表底部。
    - top: 顶部 X 轴。
    - left: 左侧 Y 轴，通常作为默认主 Y 轴，用于展示主要数值指标。
    - right: 右侧 Y 轴，通常用于双 Y 轴图表、辅助数值轴、不同量纲指标对比等。

笛卡尔坐标系中的坐标轴通常遵循：
    - X 轴：`bottom` 或 `top`。
    - Y 轴：`left` 或 `right`。

在 Athena Charts 中：
    - X 轴可以使用时间类型、日期类型、数值类型、分类类型。
    - Y 轴通常只能使用数值类型。
"""

type PolarAxisRole = Literal["theta", "radius"]
"""极坐标轴角色定义。

取值说明：
    - theta: 角度轴，用于描述数据在极坐标系中的角度方向，通常对应分类、时间、日期或数值型角度数据。
    - radius: 半径轴，用于描述数据距离极坐标中心点的距离，通常应为数值类型。

在极坐标系中 `theta` 决定方向，`radius` 决定距离。
"""


type TickLabelFormatKind = Literal["auto", "datetime", "date", "time", "number", "category", "percent", "currency"]
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
`TickLabelFormatKind="time"` 表示刻度标签仅显示时间部分。
"""


type TickLocatorStrategy = Literal["auto", "all", "fixed", "none"]
"""刻度位置选择策略，用于描述坐标轴刻度值如何选择。

取值说明：
    - auto: 自动选择刻度，由渲染引擎根据坐标轴数据类型、数据范围、图表尺寸和 `max_count` 等信息自动决定刻度数量与位置。
        这是默认策略，适合大多数场景。
    - all: 展示所有候选刻度值，通常适用于分类数量较少，或者用户明确希望展示每一个数据点刻度的场景。
    - fixed: 使用固定刻度值，刻度值由 `TickLocator.fixed_values` 明确指定。
    - none: 不生成刻度，通常用于隐藏刻度位置，但是否隐藏刻度标签仍由 `TickOptions.visible` 和 `TickOptions.label_visible` 共同决定。

注意：
    该类型描述的是“刻度位置选择策略”，不负责刻度标签文本格式化，刻度标签文本格式化应由 `TickLabelFormat` 描述。
"""
