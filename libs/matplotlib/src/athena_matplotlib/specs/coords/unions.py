from typing import Annotated

from pydantic import Field

from athena_matplotlib.specs.coords.cartesian import CartesianCoord
from athena_matplotlib.specs.coords.polar import PolarCoord

type CoordSpec = Annotated[
    CartesianCoord | PolarCoord,
    Field(discriminator="kind"),
]
"""坐标系规范联合类型，用于描述图表所使用的坐标系 coordinate system。

`CoordSpec` 是一个基于 `kind` 字段的可判别联合类型 (discriminated union)，用于在运行时自动解析为具体坐标系类型。

支持的坐标系类型：
    - `"cartesian"` → `CartesianCoord`
    - `"polar"` → `PolarCoord`

坐标系负责定义：
    - 坐标轴结构
    - 数据空间映射方式
    - 刻度与网格规则
    - 坐标系布局
    - Plot 的可绘制范围

不同坐标系允许的 Plot 类型通常不同：
    - `CartesianCoord`：
        - 折线图
        - 柱状图
        - 面积图
        - 散点图
        - 组合图

    - `PolarCoord`：
        - 饼图
        - 环形图
        - 雷达图
        - 极坐标柱状图

一个 Chart 在同一时刻只能使用一个坐标系，但可以在同一个坐标系中绘制多个兼容的 Plot，例如：
    - `LinePlot` 与 `BarPlot` 可以同时绘制在 `CartesianCoord` 中。
    - `PiePlot` 通常只能绘制在 `PolarCoord` 中。
"""
