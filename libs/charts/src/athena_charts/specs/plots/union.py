from typing import Annotated

from pydantic import Field

from athena_charts.specs.plots.bar import BarPlot
from athena_charts.specs.plots.line import LinePlot
from athena_charts.specs.plots.pie import PiePlot

type PlotSpec = Annotated[LinePlot | BarPlot | PiePlot, Field(discriminator="kind")]
