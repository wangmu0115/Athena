from typing import Literal

from pydantic import Field

from athena_charts.plots import PolarPlot
from athena_charts.plots.data import PiePlotData
from athena_charts.plots.options import PiePlotOptions


class PiePlot(PolarPlot):
    kind: Literal["pie"] = Field("pie", description="饼图")
    data: PiePlotData = Field(..., description="饼图数据")
    options: PiePlotOptions = Field(default_factory=PiePlotOptions, description="饼图配置")
