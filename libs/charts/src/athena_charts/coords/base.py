from typing import Literal

from pydantic import Field

from athena_core.models import BaseAthenaModel

type CoordKind = Literal["cartesian", "polar"]


class Coord(BaseAthenaModel):
    kind: CoordKind = Field(..., description="坐标系统类型")
