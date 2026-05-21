from pydantic import Field

from athena_charts.themes._base import _BaseTheme
from athena_charts.themes.types import FontWeight, LineStyle, TickDirection


class TickTheme(_BaseTheme):
    tick_color: str | None = Field(None, description="刻度线颜色")
    tick_width: float | None = Field(None, gt=0, description="刻度线宽度")
    tick_length: float | None = Field(None, gt=0, description="刻度线长度")
    tick_direction: TickDirection | None = Field(None, description="刻度线朝向")
    label_fontsize: int | None = Field(None, gt=0, description="刻度文本字号")
    label_fontweight: FontWeight | None = Field(None, description="刻度文本字体粗细")
    label_color: str | None = Field(None, description="刻度文本颜色")
    label_rotation: float | None = Field(None, ge=-90, le=90, description="刻度文本旋转角度")


class GridTheme(_BaseTheme):
    line_color: str | None = Field(None, description="网格线颜色")
    line_width: float | None = Field(None, gt=0, description="网格线宽度")
    line_style: LineStyle | None = Field(None, description="网格线样式")
    alpha: float | None = Field(None, ge=0, le=1, description="网格线透明度")


class AxisTheme(_BaseTheme):
    line_color: str | None = Field(None, description="坐标轴线颜色")
    line_width: float | None = Field(None, gt=0, description="坐标轴线宽度")
    label_fontsize: int | None = Field(None, gt=0, description="坐标轴标题字号")
    label_fontweight: FontWeight | None = Field(None, description="坐标轴标题字体粗细")
    label_color: str | None = Field(None, description="坐标轴标题文本颜色")
