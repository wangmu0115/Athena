from typing import Literal

from pydantic import Field

from athena_charts.options.base import Options


class PlotOptions(Options):
    opacity: float | None = Field(None, ge=0, le=1, description="透明度")
    show_data_labels: bool = Field(False, description="是否显示数据")


class CartesianPlotOptions(PlotOptions):
    y_axis_side: Literal["left", "right"] = Field("left", description="使用左侧或右侧 Y 轴")


class LinePlotOptions(CartesianPlotOptions):
    line_width: float | None = Field(None, gt=0, description="折线宽度")
    line_style: Literal["solid", "dashed", "dotted", "dashdot"] | None = Field(None, description="线型")
    show_marker: bool | None = Field(None, description="是否显示数据点")
    marker: str | None = Field(None, description="标记样式")
    marker_size: float | None = Field(None, gt=0, description="标记大小")


class BarPlotOptions(CartesianPlotOptions):
    mode: Literal["group", "stack", "overlay"] = Field("group", description="柱状图布局模式")
    bar_width: float | None = Field(None, gt=0, description="柱宽")
    edge_width: float | None = Field(None, ge=0, description="边框宽度")


class PiePlotOptions(PlotOptions):
    donut: bool = Field(False, description="是否为环形图")
    inner_radius: float | None = Field(None, ge=0, le=1, description="内半径比例")
    start_angle: float | None = Field(None, description="起始角度")
    clockwise: bool | None = Field(None, description="是否顺时针")
    show_label: bool | None = Field(None, description="是否显示标签")
    show_percentage: bool | None = Field(None, description="是否显示百分比")
