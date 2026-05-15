from typing import Literal

from pydantic import Field

from athena_charts.specs.coords import Coord
from athena_charts.specs.plots.base import Plot
from athena_charts.specs.plots.data import BarPlotData
from athena_charts.specs.plots.options import BarPlotOptions


class BarPlot(Plot):
    kind: Literal["bar"] = Field("bar", description="柱状图")
    coord_kind: Literal["cartesian"] = Field("cartesian", description="笛卡尔坐标系")
    data: BarPlotData = Field(..., description="图层数据")
    options: BarPlotOptions = Field(default_factory=BarPlotOptions, description="柱状图配置")

    def validate_with_coord(self, coord: Coord):
        super().validate_with_coord(coord)
        if coord.get_y_axis(self.options.y_axis_side) is None:
            raise ValueError(f"Plot {self.name or self.kind} uses {self.options.y_axis_side} Y axis, but coord does not define it.")
