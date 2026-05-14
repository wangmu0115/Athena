
from typing import Literal

from athena_core.models.base import BaseAthenaModel
from pydantic import Field


type CoordKind = Literal["cartesian", "polar"]

class Coord(BaseAthenaModel):
    kind: CoordKind = Field(..., description="坐标系统类型")