
from typing import Literal

from athena_core.models.base import BaseAthenaModel
from pydantic import Field


class PlotOptions(BaseAthenaModel):
    opacity: float = Field(1.0, ge=0, le=1, description="透明度")
    show_data_labels: bool = Field(False, description="是否显示数据")

class CartesianPlotOptions(PlotOptions):
    y_axis_side: Literal["left", "right"] = Field("left", description="使用左侧或右侧 Y 轴")

class LinePlotOptions(CartesianPlotOptions):
    line_width: float = Field(1.5, gt=0, description="折线宽度")
    line_style: Literal["solid", "dashed", "dotted", "dashdot"] = Field("solid", description="线型")
    show_marker: bool = Field(False, description="是否显示数据点")
    marker_size: float = Field(3.0, gt=0, description="数据点大小")