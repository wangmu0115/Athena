from typing import Literal

from pydantic import Field

from athena_charts.plots import CartesianPlot, LinePlotOptions


class LinePlot(CartesianPlot):
    kind: Literal["line"] = Field("line", description="折线图")
    options: LinePlotOptions = Field(default_factory=LinePlotOptions, description="折线图配置")
