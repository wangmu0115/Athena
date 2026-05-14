from pydantic import Field

from athena_core.models import BaseAthenaModel


class FigureTheme(BaseAthenaModel):
    background_color: str = Field("white", description="画布背景颜色")
    title_font_size: int = Field(13, gt=0, description="画布标题字号")
    subtitle_font_size: int = Field(11, gt=0, description="画布副标题字号")
