from typing import Literal

from pydantic import Field

from athena_charts.coords import Coord


class CartesianCoord(Coord):
    kind: Literal["cartesian"] = Field("cartesian", description="笛卡尔坐标系")
