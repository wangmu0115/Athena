from typing import Annotated, Literal

from pydantic import Field

from athena_charts.coords import CartesianCoord, PolarCoord
from athena_core.models import BaseAthenaModel

type CoordKind = Literal["cartesian", "polar"]

type CoordSpec = Annotated[CartesianCoord | PolarCoord, Field(discriminator="kind")]


class Coord(BaseAthenaModel):
    kind: CoordKind = Field(..., description="坐标系统类型")
