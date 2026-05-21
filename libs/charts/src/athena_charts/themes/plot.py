from pydantic import Field

from athena_charts.themes._base import _BaseTheme


class PlotTheme(_BaseTheme):
    opacity: float | None = Field(None, ge=0, le=1, description="默认透明度")
    line_width: float | None = Field(None, gt=0, description="默认线宽")
    marker_size: float | None = Field(None, gt=0, description="默认标记大小")
    bar_width: float | None = Field(None, gt=0, le=1, description="默认柱宽")
