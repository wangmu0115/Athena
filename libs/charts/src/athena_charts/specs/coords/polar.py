from typing import Literal

from pydantic import Field

from athena_charts.specs.coords.axis import AxisSpec
from athena_charts.specs.coords.base import Coord


class PolarAxisSpec(AxisSpec):
    """极坐标轴：角度轴 (theta) 和半径轴 (radius)"""

    role: Literal["theta", "radius"] = Field(..., description="极坐标轴角色")


class PolarCoord(Coord):
    kind: Literal["polar"] = Field("polar", description="极坐标系")
    angle_axis: PolarAxisSpec | None = Field(None, description="角度轴")
    radius_axis: PolarAxisSpec | None = Field(None, description="半径轴")
