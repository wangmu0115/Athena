from typing import Literal

from pydantic import Field

from athena_charts.options.base import Options

LegendPosition = Literal[
    "auto",
    "top",
    "bottom",
    "left",
    "right",
    "inside_top_left",
    "inside_top_right",
    "inside_bottom_left",
    "inside_bottom_right",
]


class LegendOptions(Options):
    visible: bool | None = Field(None, description="是否显示图例")
    title: str | None = Field(None, description="图例标题")
    position: LegendPosition | None = Field(None, description="图例位置")
    columns: int | None = Field(None, gt=0, description="图例列数")


class ChartOptions(Options):
    title: str | None = Field(None, description="图表标题")
    subtitle: str | None = Field(None, description="图表副标题")
    clip_overflow: bool | None = Field(None, description="是否裁剪超出绘图区的内容")
    legend: LegendOptions = Field(default_factory=LegendOptions, description="图例配置")
