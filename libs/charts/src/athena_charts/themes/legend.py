from pydantic import Field

from athena_charts.themes._base import _BaseTheme
from athena_charts.themes.types import FontWeight, LegendDirection, LegendLocation


class LegendTheme(_BaseTheme):
    location: LegendLocation | None = Field(None, description="图例位置")
    direction: LegendDirection | None = Field(None, description="图例排列方向")
    title_fontsize: int | None = Field(None, gt=0, description="图例标题字号")
    title_fontweight: FontWeight | None = Field(None, description="图例标题字体粗细")
    title_color: str | None = Field(None, description="图例标题文本颜色")
    label_fontsize: int | None = Field(None, gt=0, description="图例文本字号")
    label_fontweight: FontWeight | None = Field(None, description="图例文本字体粗细")
    label_color: str | None = Field(None, description="图例文本颜色")
    background_color: str | None = Field(None, description="图例背景颜色")
    edge_color: str | None = Field(None, description="图例边框颜色")
    edge_width: float | None = Field(None, gt=0, description="图例边框宽度")
    alpha: float | None = Field(None, ge=0, le=1, description="图例透明度")
