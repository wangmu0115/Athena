from typing import Literal

from pydantic import Field

from athena_charts.coords import Coord, PolarAxis


class PolarCoord(Coord):
    kind: Literal["polar"] = Field("polar", description="极坐标系")

    angle_axis: PolarAxis | None = Field(None, description="角度轴")
    radius_axis: PolarAxis | None = Field(None, description="半径轴")
