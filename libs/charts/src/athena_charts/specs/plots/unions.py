from typing import Annotated

from pydantic import Field

from athena_charts.specs.plots.bar import BarPlot
from athena_charts.specs.plots.line import LinePlot
from athena_charts.specs.plots.pie import PiePlot

type PlotSpec = Annotated[
    LinePlot | BarPlot | PiePlot,
    Field(discriminator="kind"),
]
"""图层规范联合类型，用于描述图表中的具体绘制图层 Plot。

`PlotSpec` 是一个基于 `kind` 字段的可判别联合类型 (discriminated union)，用于在运行时自动解析为具体图层类型。

支持的图层类型：
    - `"line"` → `LinePlot`
    - `"bar"` → `BarPlot`
    - `"pie"` → `PiePlot`

图层 Plot 是图表中的最小绘制单元，负责描述：
    - 数据内容
    - 数据与坐标的映射关系
    - 图层样式
    - 图层渲染方式

多个 Plot 可以组合绘制在同一个 Chart 中，但必须满足：
    - 使用相同坐标系类型
    - 使用兼容的数据映射方式
"""
