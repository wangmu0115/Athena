from pydantic import Field

from athena_charts.specs._base import _BaseSpec
from athena_charts.specs.coords import Coord, CoordKind
from athena_charts.specs.plots.types import PlotKind


class Plot(_BaseSpec):
    kind: PlotKind = Field(..., description="图层类型")
    coord_kind: CoordKind = Field(..., description="图层所属坐标系统")
    name: str = Field("", description="图层名称，通常用于图例")
    z_index: int = Field(0, description="图层顺序，值越小图层越在底部")

    def validate_coord(self, coord: Coord):
        """验证绘制图层的坐标系"""
        if self.coord_kind != coord.kind:
            raise ValueError(f"Plot {self.name or self.kind} requires {self.coord_kind} coordinate system.")
