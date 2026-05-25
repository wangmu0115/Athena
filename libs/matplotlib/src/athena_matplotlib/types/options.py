from typing import Literal

type ImageFormat = Literal["png", "jpg", "jpeg", "svg", "pdf", "eps", "ps", "webp"]
"""图片输出格式，用于描述图表导出时的目标图片格式。

取值说明：
    - png: PNG 位图格式，支持透明背景，最常用。
    - jpg: JPEG 位图格式，适用于照片类图像，不支持透明背景。
    - jpeg: JPEG 位图格式，与 `jpg` 等价。
    - svg: SVG 矢量图格式，适用于网页和高分辨率缩放场景。
    - pdf: PDF 矢量文档格式，适用于论文、报告和打印输出。
    - eps: EPS 矢量图格式，常用于学术出版。
    - ps: PostScript 矢量图格式。
    - webp: WebP 图片格式，压缩率较高。

推荐：
    - 通用图片输出使用 `png`。
    - 学术论文使用 `pdf` 或 `svg`。
    - Web 场景使用 `svg` 或 `webp`。
"""

type BboxInches = Literal["tight", "standard"]
"""图像边界框模式，用于描述图表导出时的边界裁剪方式。

取值说明：
    - tight: 自动裁剪图像周围的空白区域，使输出图片尽可能紧凑。
    - standard: 使用标准画布边界输出，不进行自动裁剪。

说明：
    - 当使用 `tight` 时，标题、图例、坐标轴标签等元素会被自动纳入边界计算。
    - `tight` 常用于导出报告图片或 Markdown 内嵌图表，避免图表周围存在大量空白。
    - `standard` 更适合多子图布局，固定尺寸输出和需要保持统一画布比例的场景。

注意：
    - `tight` 模式可能会改变最终输出图片的实际尺寸。
    - 某些复杂布局下，`tight` 可能导致图例、注释或文本位置发生轻微变化。
"""
