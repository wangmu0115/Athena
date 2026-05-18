from typing import Literal

from pydantic import Field

from athena_charts_matplotlib.options.base import BaseOptions


class MatplotlibSavingOptions(BaseOptions):
    dpi: int | None = Field(None, gt=0, description="输出分辨率，每英寸点数")
    format: Literal["png", "svg", "pdf"] | None = Field(None, description="输出图片格式")
    bbox_inches: Literal["tight", "standard"] | None = Field(None, description="输出图片的边界框，对应`bbox_inches`")
    pad_inches: float | None = Field(None, ge=0, description="当 bbox_inches 设置为 tight 时，图形周围的内边距，单位 inch")
    transparent: bool | None = Field(None, description="是否透明背景")
