from pydantic import Field

from athena_core.models import BaseAthenaModel


class PlotTheme(BaseAthenaModel):
    line_width: float = Field(1.5, gt=0, description="默认线宽")
    marker_size: float = Field(3.0, gt=0, description="默认标记大小")
    bar_width: float = Field(0.8, gt=0, le=1, description="默认柱宽")
