from pydantic import Field

from athena_charts.themes._base import _BaseTheme
from athena_charts.themes.types import LineStyle


class PlotTheme(_BaseTheme):
    opacity: float | None = Field(None, ge=0, le=1, description="默认透明度")
    line_width: float | None = Field(None, gt=0, description="默认线宽")
    line_style: LineStyle | None = Field(None, description="默认线型")
    marker_size: float | None = Field(None, gt=0, description="默认标记大小")
    marker_edgecolor: str | None = Field(None, description="默认标记边框颜色")
    marker_edgewidth: float | None = Field(None, gt=0, description="默认标记边框宽度")
    bar_width: float | None = Field(None, gt=0, le=1, description="默认柱宽")
    bar_edgecolor: str | None = Field(None, description="默认柱子边框颜色")
    bar_edgewidth: float | None = Field(None, gt=0, description="默认柱子边框宽度")
