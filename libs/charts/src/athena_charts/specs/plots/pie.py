from typing import Literal

from pydantic import Field

from athena_charts.specs.plots.base import Plot
from athena_charts.specs.plots.data import PiePlotData
from athena_charts.specs.plots.options import PiePlotOptions


class PiePlot(Plot):
    kind: Literal["pie"] = Field("pie", description="饼图")
    coord_kind: Literal["polar"] = Field("polar", description="极坐标系")
    data: PiePlotData = Field(..., description="饼图数据")
    options: PiePlotOptions = Field(default_factory=PiePlotOptions, description="饼图配置")
