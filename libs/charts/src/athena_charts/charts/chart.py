from typing import Self

from pydantic import Field, model_validator

from athena_charts.charts import ChartLabels, ChartOptions
from athena_charts.coords import Coord
from athena_charts.plots import Plot
from athena_core.models import BaseAthenaModel


class Chart(BaseAthenaModel):
    labels: ChartLabels = Field(default_factory=ChartLabels, description="图表文本标签")
    coord: Coord = Field(..., description="坐标系统")
    plots: list[Plot] = Field(default_factory=list, description="图层列表")
    options: ChartOptions = Field(default_factory=ChartOptions, description="图表配置")

    @model_validator(mode="after")
    def validate_coord_and_plots(self) -> Self:
        if not self.plots:
            raise ValueError("Chart must contain at least one plot.")

        for plot in self.plots:
            if plot.coord_kind != self.coord.kind:
                raise ValueError(f"Plot {plot.kind} requires coord {plot.coord_kind}, but chart coord is {self.coord.kind}.")

        return self
