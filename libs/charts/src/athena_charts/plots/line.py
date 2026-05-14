
from typing import Literal

from athena_charts.plots.base import CartesianPlot
from athena_charts.plots.options import LinePlotOptions
from pydantic import Field


class LinePlot(CartesianPlot):
    kind: Literal["line"] = Field("line", description="折线图")
    options: LinePlotOptions = Field(default_factory=LinePlotOptions, description="折线图配置")