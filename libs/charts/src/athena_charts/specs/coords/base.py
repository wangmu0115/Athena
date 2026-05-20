from pydantic import Field

from athena_charts.specs._base import _BaseSpec
from athena_charts.specs.coords.types import CoordKind


class Coord(_BaseSpec):
    kind: CoordKind = Field(..., description="坐标系统类型")
