from typing import Literal

from pydantic import Field

from athena_charts.plots import BarPlotOptions, CartesianPlot


class BarPlot(CartesianPlot):
    kind: Literal["bar"] = Field("bar", description="柱状图")
    options: BarPlotOptions = Field(default_factory=BarPlotOptions, description="柱状图配置")
