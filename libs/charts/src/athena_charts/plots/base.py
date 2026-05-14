from typing import Annotated, Literal

from pydantic import Field

from athena_charts.coords import CoordKind
from athena_charts.plots import (
    BarPlot,
    LinePlot,
    PiePlot,
)
from athena_core.models import BaseAthenaModel

type PlotKind = Literal["line", "bar", "pie"]

type PlotSpec = Annotated[LinePlot | BarPlot | PiePlot, Field(discriminator="kind")]


class Plot(BaseAthenaModel):
    name: str = Field("", description="图层名称，通常用于图例")
    kind: PlotKind = Field(..., description="图层类型")
    coord_kind: CoordKind = Field(..., description="图层所属坐标系统")
