from typing import Literal, Self

from pydantic import Field, model_validator

from athena_charts.specs._base import _BaseSpec


class XYPoint(_BaseSpec):
    """二维坐标轴中的点"""

    x: object = Field(..., description="X 轴值")
    y: float | None = Field(..., description="Y 轴值")


class CategoricalDatum(_BaseSpec):
    """分类数据项"""

    category: str = Field(..., description="分类名称")
    value: float | None = Field(None, description="分类数值")


class XYSeriesData(_BaseSpec):
    kind: Literal["xy"] = "xy"
    x: list[object] = Field(..., description="X 轴数据")
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
    def validate(self) -> Self:
        if not self.x or not self.y:
            raise ValueError("XYSeriesData cannot be empty.")
        if len(self.x) != len(self.y):
            raise ValueError("XYSeriesData.x and XYSeriesData.y must have the same length.")
        return self


class CategoricalSeriesData(_BaseSpec):
    kind: Literal["categorical"] = "categorical"
    datums: list[CategoricalDatum] = Field(..., description="分类项列表")

    @model_validator(mode="after")
    def validate(self) -> Self:
        if not self.datums:
            raise ValueError("CategoricalSeriesData cannot be empty.")
        return self

    @property
    def categories(self) -> list[str]:
        return [datum.category for datum in self.datums]

    @property
    def values(self) -> list[float | None]:
        return [datum.value for datum in self.datums]
