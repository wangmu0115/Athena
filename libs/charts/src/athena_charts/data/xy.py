from typing import Any, Literal, Self

from pydantic import Field, model_validator

from athena_core.models import BaseAthenaModel


class XYPoint(BaseAthenaModel):
    """二维坐标轴中的点"""

    x: Any = Field(..., description="X 轴值")
    y: float | None = Field(..., description="Y 轴值")


class XYSeriesData(BaseAthenaModel):
    kind: Literal["xy"] = "xy"  # For Serialization and Deserialization in BarPlotData

    x: list[Any] = Field(..., description="X 轴数据")
    y: list[float | None] = Field(..., description="Y 轴数据")

    @classmethod
    def from_points(cls, points: list[XYPoint]):
        x = []
        y = []
        for point in points or []:
            x.append(point.x)
            y.append(point.y)
        return cls(x=x, y=y)

    @model_validator(mode="after")
    def validate_model(self) -> Self:
        if not self.x or not self.y:
            raise ValueError("XYSeriesData cannot be empty.")

        if len(self.x) != len(self.y):
            raise ValueError("XYSeriesData.x and XYSeriesData.y must have the same length.")

        return self
