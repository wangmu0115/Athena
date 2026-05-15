from typing import Self

from pydantic import Field, model_validator

from athena_charts.specs.charts.labels import ChartLabels
from athena_charts.specs.charts.options import ChartOptions
from athena_charts.specs.coords import CartesianCoord, CoordSpec
from athena_charts.specs.plots import PlotSpec
from athena_core.models import BaseAthenaModel


class ChartSpec(BaseAthenaModel):
    labels: ChartLabels = Field(default_factory=ChartLabels, description="图表文本标签")
    coord: CoordSpec = Field(..., description="坐标系统")
    plots: list[PlotSpec] = Field(default_factory=list, description="图层列表")
    options: ChartOptions = Field(default_factory=ChartOptions, description="图表配置")

    @model_validator(mode="after")
    def validate_coord_and_plots(self) -> Self:
        if not self.plots:
            raise ValueError("Chart must contain at least one plot.")

        is_cartesian_coord = isinstance(self.coord, CartesianCoord)
        for plot in self.plots:
            if plot.coord_kind != self.coord.kind:
                raise ValueError(f"Plot {plot.kind} requires coord {plot.coord_kind}, but chart coord is {self.coord.kind}.")

            if is_cartesian_coord and hasattr(plot.options, "y_axis_side") and not self.coord.get_y_axis(plot.options.y_axis_side):
                raise ValueError(f"Plot {plot.name or plot.kind} uses {plot.options.y_axis_side} Y axis, but chart coord does not define it.")

        return self
