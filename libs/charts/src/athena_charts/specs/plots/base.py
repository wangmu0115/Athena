from typing import Literal

from pydantic import Field

from athena_charts.specs.coords import Coord, CoordKind
from athena_core.models import BaseAthenaModel

type PlotKind = Literal["line", "bar", "pie"]


class Plot(BaseAthenaModel):
    name: str = Field("", description="图层名称，通常用于图例")
    kind: PlotKind = Field(..., description="图层类型")
    coord_kind: CoordKind = Field(..., description="图层所属坐标系统")

    def validate_with_coord(self, coord: Coord):
        if self.coord_kind != coord.kind:
            raise ValueError(f"Plot {self.kind} requires coord {self.coord_kind}.")
