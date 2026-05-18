from pydantic import Field

from athena_charts.themes.base import BaseTheme, FontWeight


class FigureTheme(BaseTheme):
    background_color: str | None = Field(None, description="画布背景颜色")
    edge_color: str | None = Field(None, description="画布边框颜色")
    title_font_size: int | None = Field(None, gt=0, description="画布标题字号")
    subtitle_font_size: int | None = Field(None, gt=0, description="画布副标题字号")
    title_font_weight: FontWeight | None = Field(None, description="画布标题字体粗细")
