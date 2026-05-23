from typing import Literal

type FontFamily = Literal["sans-serif", "serif", "monospace", "cursive", "fantasy"]
"""Matplotlib 字体族类型，用于指定 Matplotlib 文本的字体族 `font.family`。

这些值并不直接对应某一个具体字体文件，Matplotlib 会根据当前配置，如 `font.sans-serif` 在系统已安装字体中依次查找并匹配可用字体。

可选值：
    - sans-serif: 无衬线字体，Matplotlib 默认字体族，字形边缘干净、现代，适合数据可视化与屏幕阅读。常见字体：
        - `DejaVu Sans`
        - `Arial`
        - `Helvetica`
        - `PingFang SC`
        - `Microsoft YaHei`
        - `Noto Sans CJK SC`
    - serif: 衬线字体，字符边缘带有装饰性衬线，更适合正式文档、出版物或印刷风格图表。常见字体：
        - `Times New Roman`
        - `Georgia`
        - `Songti SC`
        - `STSong`
    - monospace: 等宽字体，每个字符占用相同宽度，常用于代码、终端输出、表格对齐等场景。常见字体：
        - `Consolas`
        - `Menlo`
        - `Courier New`
        - `Monaco`
    - cursive: 手写/草书风格字体，常用于装饰性文本，在数据图表中较少使用。
    - fantasy: 装饰性/艺术风格字体，风格较强，适合特殊视觉效果，不推荐用于正式数据可视化。

注意：
    `font.family` 指定的是“字体族”，不是具体字体名称，若希望控制实际使用的字体，需要同时配置对应的字体列表：
        - `font.sans-serif`
        - `font.serif`
        - `font.monospace`

    当指定字体不存在时，Matplotlib 会自动回退到下一个可用字体。
"""

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


type LineStyle = Literal["solid", "dashed", "dotted", "dashdot", "none"]
"""线条样式定义，用于描述图表中线条的绘制风格。

取值说明：
    - solid: 实线，使用连续线段绘制，是最常见的线条样式。
    - dashed: 虚线，使用较长间隔的断续线段绘制。
    - dotted: 点线，使用短点状线段绘制。
    - dashdot: 点划线，使用“虚线 + 点线”组合绘制。
    - none: 不显示线
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


type MarkerShape = Literal["circle", "square", "triangle", "diamond", "cross", "plus", "star", "none"]
"""数据点标记形状定义，用于描述图层中数据点的可视化标记样式。

取值说明：
    - circle: 圆形标记，最常见的数据点标记形式。
    - square: 方形标记，适合强调离散数据点。
    - triangle: 三角形标记。
    - diamond: 菱形标记。
    - cross: 叉形标记。
    - plus: 加号形标记。
    - star: 星形标记。
    - none: 不显示标记。
"""


type GridAxis = Literal["x", "y", "both"]
"""网格线应用坐标轴范围，用于控制网格线应用到哪些坐标轴方向。

可选值：
- x: 仅为 X 轴刻度绘制网格线，最终显示为竖向网格线。
- y: 仅为 Y 轴刻度绘制网格线，最终显示为横向网格线。
- both: 同时为 X/Y 两个方向绘制网格线，即同时显示竖向网格线和横向网格线。
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


type HorizontalAlignment = Literal["left", "right", "center"]
"""水平对齐方式，用于描述文本、标签或图形元素在水平方向上的对齐位置。

常见用于：
    - 图表标题 Title
    - 坐标轴标签 Axis Label
    - 数据标签 Data Label
    - 注释 Annotation 
    - 图例文本 Legend

取值说明：
    - left: 左对齐。
    - center: 水平居中对齐。
    - right: 右对齐。
"""

type VerticalAlignment = Literal["top", "center", "bottom"]
"""垂直对齐方式，用于描述文本、标签或图形元素在垂直方向上的对齐位置。

常见用于：
    - 坐标轴标签 Axis Label
    - 数据标签 Data Label
    - 注释 Annotation
    - 文本框 Text Box

取值说明：
    - top: 顶部对齐。
    - center: 垂直居中对齐。
    - bottom: 底部对齐。
"""
