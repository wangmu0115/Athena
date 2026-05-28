from dataclasses import dataclass
from typing import Literal, Self

from pydantic import Field, model_validator

from athena_matplotlib.specs._base import _BaseSpec


@dataclass
class XYPoint:
    x: object
    """X 轴值"""
    y: float | None
    """Y 轴值"""

    @classmethod
    def point(cls, *, x: object, y: float | None):
        return cls(x=x, y=y)


class XYSeriesData(_BaseSpec):
    kind: Literal["xy"] = "xy"
    x: list[object] = Field(..., description="X 轴数据")
    y: list[float | None] = Field(..., description="Y 轴数据")

    @classmethod
    def from_points(cls, points: list[XYPoint]) -> Self:
        x = []
        y = []
        for point in points or []:
            x.append(point.x)
            y.append(point.y)
        return cls(x=x, y=y)

    @classmethod
    def of(cls, x: list[object], y: list[float | None]) -> Self:
        return cls(x=x, y=y)

    @model_validator(mode="after")
    def validate(self) -> Self:
        if not self.x or not self.y:
            raise ValueError("XYSeriesData cannot be empty.")
        if len(self.x) != len(self.y):
            raise ValueError("XYSeriesData.x and XYSeriesData.y must have the same length.")
        return self
