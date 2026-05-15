from pydantic import Field

from athena_core.models import BaseAthenaModel


class FigureOptions(BaseAthenaModel):
    width: int = Field(1600, gt=0, description="画布宽度，单位 px")
    height: int = Field(960, gt=0, description="画布高度，单位 px")
    background_color: str = Field("white", description="画布背景色")
