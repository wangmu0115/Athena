from typing import Literal

from pydantic import Field

from athena_charts.plots import BarPlotOptions, Plot, XYPlotData


class BarPlot(Plot):
    kind: Literal["bar"] = Field("bar", description="柱状图")
    coord_kind: Literal["cartesian"] = Field("cartesian", description="笛卡尔坐标系")
    data: XYPlotData = Field(..., description="图层数据")
    options: BarPlotOptions = Field(default_factory=BarPlotOptions, description="柱状图配置")
