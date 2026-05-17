from typing import Literal

from pydantic import Field

from athena_core.models.base import BaseAthenaModel

FontWeight = Literal["ultralight", "light", "normal", "medium", "semibold", "bold", "heavy", "black"]


class Options(BaseAthenaModel):
    """配置基础类"""


class MatplotlibFigureOptions(Options):
    width: int | None = Field(None, gt=0, description="画布宽度，单位 px")
    height: int | None = Field(None, gt=0, description="画布高度，单位 px")
    dpi: int | None = Field(None, gt=0, description="分辨率，每英寸点数")
    background_color: str | None = Field(None, description="画布背景颜色")
    edge_color: str | None = Field(None, description="画布边框颜色")
    title_font_size: int | None = Field(None, gt=0, description="画布标题字号")
    title_font_weight: FontWeight | None = Field(None, description="画布标题字体粗细")


ImageFormat = Literal["png", "svg", "pdf"]


class MatplotlibRenderOptions(BaseAthenaModel):
    """Matplotlib 渲染参数。

    这里只放 Matplotlib 实现细节，不放通用视觉样式。
    """

    dpi: int = Field(144, gt=0, description="输出 DPI")
    image_format: ImageFormat = Field("png", description="输出图片格式")
    bbox_inches: Literal["tight"] | None = Field("tight", description="savefig 的 bbox_inches 参数")
    constrained_layout: bool = Field(False, description="是否启用 constrained_layout")
    tight_layout: bool = Field(True, description="是否调用 figure.tight_layout()")
    rc_params: dict[str, object] = Field(default_factory=dict, description="额外 Matplotlib rcParams")


class MatplotlibOptions(Options):
    figure: MatplotlibFigureOptions
