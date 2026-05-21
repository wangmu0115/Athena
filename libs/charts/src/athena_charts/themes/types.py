from typing import Literal

type FontWeight = Literal["ultralight", "light", "normal", "medium", "semibold", "bold", "heavy", "black"]
"""字体粗细类型，用于描述图表文本的字体粗细语义，例如标题、坐标轴标签、刻度文本、图例文本、数据标签和注释文本等。

可选值：
    - ultralight: 极细字体。
    - light: 细体。
    - normal: 常规字体。
    - medium: 中等粗细。
    - semibold: 半粗体。
    - bold: 粗体。
    - heavy: 特粗体。
    - black: 最粗字体。
"""


type TickDirection = Literal["out", "in", "inout"]
"""刻度线朝向。

可选值：
    - out: 刻度线向坐标轴外侧延伸。
    - in: 刻度线向坐标轴内侧延伸。
    - inout: 刻度线同时向内外两侧延伸。
"""


type LegendLocation = Literal["auto", "top", "bottom", "left", "right", "top_left", "top_right", "bottom_left", "bottom_right", "center"]
"""图例位置类型，用于描述图例在图表中的布局位置。

取值说明：
    - auto: 自动选择图例位置，由渲染引擎根据图表布局自动决定。
    - top: 位于图表顶部居中区域。
    - bottom: 位于图表底部居中区域。
    - left: 位于图表左侧居中区域。
    - right: 位于图表右侧居中区域。
    - top_left: 位于图表左上角。
    - top_right: 位于图表右上角。
    - bottom_left: 位于图表左下角。
    - bottom_right: 位于图表右下角。
    - center: 位于图表中心区域。
"""


type LegendDirection = Literal["horizontal", "vertical"]
"""图例排列方向，用于描述多个图例项的排列方式。

取值说明：
    - horizontal: 水平排列，图例项从左到右依次布局。
    - vertical: 垂直排列，图例项从上到下依次布局。

说明：
    - 水平排列通常适用于顶部或底部图例。
    - 垂直排列通常适用于左右侧图例。
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
