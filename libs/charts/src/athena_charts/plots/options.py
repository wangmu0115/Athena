from typing import Literal

from pydantic import Field

from athena_core.models import BaseAthenaModel


class PlotOptions(BaseAthenaModel):
    opacity: float = Field(1.0, ge=0, le=1, description="透明度")
    show_data_labels: bool = Field(False, description="是否显示数据")


class CartesianPlotOptions(PlotOptions):
    y_axis_side: Literal["left", "right"] = Field("left", description="使用左侧或右侧 Y 轴")


class PolarPlotOptions(PlotOptions):
    pass


class LinePlotOptions(CartesianPlotOptions):
    line_width: float = Field(1.5, gt=0, description="折线宽度")
    line_style: Literal["solid", "dashed", "dotted", "dashdot"] = Field("solid", description="线型")
    show_marker: bool = Field(False, description="是否显示数据点")
    marker_size: float = Field(3.0, gt=0, description="数据点大小")


class BarPlotOptions(CartesianPlotOptions):
    mode: Literal["group", "stack", "overlay"] = Field("group", description="柱状图布局模式")
    bar_width: float | None = Field(None, gt=0, description="柱宽")


class PiePlotOptions(PolarPlotOptions):
    inner_radius: float = Field(0.0, ge=0, lt=1, description="内半径比例，>0 时表示环图(donut)，=0 时表示饼图(pie)")
    start_angle: float = Field(90.0, description="起始角度")
    clockwise: bool = Field(False, description="是否顺时针绘制")
    show_percent: bool = Field(True, description="是否显示百分比")
    show_labels: bool = Field(True, description="是否显示标签")
