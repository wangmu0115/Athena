from athena_core.models import BaseAthenaModel
from pydantic import Field


class FigureOptions(BaseAthenaModel):
    width: int = Field(1600, gt=0, description="画布宽度，单位 px")
    height: int = Field(960, gt=0, description="画布高度，单位 px")
    dpi: int = Field(200, gt=0, description="输出分辨率")
    constrained_layout: bool = Field(True, description="是否启用自动约束布局")
    tight_layout: bool = Field(False, description="是否启用紧凑布局")
    transparent_background: bool = Field(False, description="是否使用透明背景")
