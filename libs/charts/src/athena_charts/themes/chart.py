from pydantic import Field

from athena_core.models import BaseAthenaModel


class GridTheme(BaseAthenaModel):
    color: str = Field("#999999", description="网格线颜色")
    alpha: float = Field(0.3, ge=0, le=1, description="网格线透明度")
    line_style: str = Field("--", description="网格线样式")
    line_width: float = Field(0.5, gt=0, description="网格线宽度")


class LegendTheme(BaseAthenaModel):
    title_font_size: int = Field(10, gt=0, description="图例标题字号")
    font_size: int = Field(8, gt=0, description="图例文本字号")


class ChartTheme(BaseAthenaModel):
    title_fontsize: int = Field(13, gt=0, description="图表标题字号")
    subtitle_font_size: int = Field(11, gt=0, description="图表副标题字号")
    background_color: str = Field("white", description="图表区域背景颜色")
