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

type GridAxis = Literal["x", "y", "both"]
"""网格线应用坐标轴范围，用于控制网格线应用到哪些坐标轴方向。

可选值：
- x: 仅为 X 轴刻度绘制网格线，最终显示为竖向网格线。
- y: 仅为 Y 轴刻度绘制网格线，最终显示为横向网格线。
- both: 同时为 X/Y 两个方向绘制网格线，即同时显示竖向网格线和横向网格线。
"""
