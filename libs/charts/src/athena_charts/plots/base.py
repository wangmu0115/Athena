from typing import Literal

from athena_charts.coords import CoordKind
from athena_charts.plots.data import XYPlotData
from athena_charts.plots.options import CartesianPlotOptions
from athena_core.models import BaseAthenaModel
from pydantic import Field


type PlotKind = Literal["line", "bar", "pie"]




class Plot(BaseAthenaModel):
    name: str = Field("", description="图层名称，通常用于图例")
    kind: PlotKind = Field(..., description="图层类型")
    coord_kind: CoordKind = Field(..., description="图层所属坐标系统")


class CartesianPlot(Plot):
    coord_kind: Literal["cartesian"] = Field("cartesian", description="笛卡尔坐标系")
    data: XYPlotData = Field(..., description="图层数据")
    options: CartesianPlotOptions = Field(default_factory=CartesianPlotOptions, description="图层配置")