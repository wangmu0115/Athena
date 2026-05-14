from typing import Literal

from pydantic import Field

from athena_charts.coords import CoordKind
from athena_charts.plots import CartesianPlotOptions, PolarPlotOptions, XYPlotData
from athena_core.models import BaseAthenaModel

type PlotKind = Literal["line", "bar", "pie"]


class Plot(BaseAthenaModel):
    name: str = Field("", description="图层名称，通常用于图例")
    kind: PlotKind = Field(..., description="图层类型")
    coord_kind: CoordKind = Field(..., description="图层所属坐标系统")


class CartesianPlot(Plot):
    coord_kind: Literal["cartesian"] = Field("cartesian", description="笛卡尔坐标系")
    data: XYPlotData = Field(..., description="图层数据")
    options: CartesianPlotOptions = Field(default_factory=CartesianPlotOptions, description="图层配置")


class PolarPlot(Plot):
    coord_kind: Literal["polar"] = Field("polar", description="极坐标系")
    options: PolarPlotOptions = Field(default_factory=PolarPlotOptions, description="图层配置")
