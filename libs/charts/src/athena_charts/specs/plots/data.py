from typing import Any, Self

from pydantic import Field, model_validator

from athena_core.models import BaseAthenaModel


class XYPoint(BaseAthenaModel):
    """二维坐标轴中的点"""

    x: Any = Field(..., description="X 轴值")
    y: float | None = Field(..., description="Y 轴值")


class CategoricalDatum(BaseAthenaModel):
    category: str = Field(..., description="分类名称")
    value: float = Field(..., ge=0, description="分类数值")


class XYSeriesData(BaseAthenaModel):
    x: list[Any] = Field(..., description="X 轴数据")
    y: list[float | None] = Field(..., description="Y 轴数据")

    @classmethod
    def from_points(cls, points: list[XYPoint]):
        if not points:
            raise ValueError("XYSeriesData cannot be empty.")
        return cls(
            x=[p.x for p in points],
            y=[p.y for p in points],
        )

    @model_validator(mode="after")
    def validate_lengths(self) -> Self:
        if len(self.x) != len(self.y):
            raise ValueError("XYSeriesData.x and XYSeriesData.y must have the same length.")
        return self


class CategoricalSeriesData(BaseAthenaModel):
    datums: list[CategoricalDatum] = Field(..., description="分类项列表")

    @property
    def categories(self) -> list[str]:
        return [datum.category for datum in self.datums]

    @property
    def values(self) -> list[float | None]:
        return [datum.value for datum in self.datums]


class LinePlotData(BaseAthenaModel):
    data: XYSeriesData = Field(..., description="XY 序列数据")


class BarPlotData(BaseAthenaModel):
    data: XYSeriesData | CategoricalSeriesData = Field(..., description="柱状图数据")


class PiePlotData(BaseAthenaModel):
    data: CategoricalSeriesData = Field(..., description="分类序列数据")

    @model_validator(mode="after")
    def validate_datums(self) -> Self:

        if sum(datum.value for datum in self.data.datums) <= 0:
            raise ValueError("PiePlotData total value must be greater than 0.")

        return self
