from pydantic import Field

from athena_charts.themes._base import _BaseTheme
from athena_charts.themes.types import FontWeight


class ChartTheme(_BaseTheme):
    background_color: str | None = Field(None, description="图表区域背景颜色")
    edge_color: str | None = Field(None, description="图表边框颜色")
    edge_linewidth: float | None = Field(None, gt=0, description="图表边框线粗")
    title_fontsize: int | None = Field(None, gt=0, description="标题字号")
    title_fontweight: FontWeight | None = Field(None, description="标题字体粗细")
    title_color: str | None = Field(None, description="标题字体颜色")
    subtitle_fontsize: int | None = Field(None, gt=0, description="副标题字号")
    subtitle_fontweight: FontWeight | None = Field(None, description="副标题字体粗细")
    subtitle_color: str | None = Field(None, description="副标题字体颜色")
