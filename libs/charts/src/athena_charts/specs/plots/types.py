from typing import Literal

type PlotKind = Literal["line", "bar", "pie"]
"""图层类型定义，用于描述图表中具体的数据绘制方式。

取值说明：
    - line: 折线图层，使用连续折线连接数据点，通常绘制于笛卡尔坐标系中。
    - bar: 柱状图层，使用矩形柱表示数据大小，通常绘制于笛卡尔坐标系中。
    - pie: 饼图图层，使用扇形区域表示数据占比，通常绘制于极坐标系中。

注意：
    PlotKind 描述的是“图层绘制类型”，而不是完整图表类型。一个 Chart 可以包含多个 Plot，但这些 Plot 必须属于相同坐标系。

例如：
    - 笛卡尔坐标系中，可以同时包含 `line` 和 `bar`。
    - 极坐标系中，通常包含 `pie`。
"""

type LineStyle = Literal["solid", "dashed", "dotted", "dashdot"]
"""线条样式定义，用于描述图表中线条的绘制风格。

取值说明：
    - solid: 实线，使用连续线段绘制，是最常见的线条样式。
    - dashed: 虚线，使用较长间隔的断续线段绘制。
    - dotted: 点线，使用短点状线段绘制。
    - dashdot: 点划线，使用“虚线 + 点线”组合绘制。

不同渲染引擎会将该抽象映射为对应的底层线型实现，例如：
    - Matplotlib:
        - `solid`   → `"-"`
        - `dashed`  → `"--"`
        - `dotted`  → `":"`
        - `dashdot` → `"-."`
    - ECharts:
        - `solid`
        - `dashed`
        - `dotted`
"""

type MarkerShape = Literal["circle", "square", "triangle", "diamond", "cross", "plus", "star"]
"""数据点标记形状定义，用于描述图层中数据点的可视化标记样式。

取值说明：
    - circle: 圆形标记，最常见的数据点标记形式。
    - square: 方形标记，适合强调离散数据点。
    - triangle: 三角形标记。
    - diamond: 菱形标记。
    - cross: 叉形标记。
    - plus: 加号形标记。
    - star: 星形标记。

注意：
    `MarkerShape` 描述的是引擎无关的语义化标记形状，不直接对应某个具体绘图库的底层 marker 实现。
    不同渲染引擎会将这些语义化形状映射为自身支持的 marker 类型。
"""
