from typing import Any, Self

from pydantic import Field, model_validator

from athena_core.models import BaseAthenaModel


class CategoricalDatum(BaseAthenaModel):
    category: str = Field(..., description="分类名称")
    value: float = Field(..., ge=0, description="数值")


class XYPlotData(BaseAthenaModel):
    x: list[Any] = Field(..., description="X 轴数据")
    y: list[float | None] = Field(..., description="Y 轴数据")

    @model_validator(mode="after")
    def validate_lengths(self) -> Self:
        if len(self.x) != len(self.y):
            raise ValueError("XYPlotData.x and XYPlotData.y must have the same length.")
        return self


class PiePlotData(BaseAthenaModel):
    datums: list[CategoricalDatum] = Field(..., description="分类项列表")

    @model_validator(mode="after")
    def validate_datums(self) -> Self:
        if not self.datums:
            raise ValueError("PiePlotData must contain at least one datum.")

        if sum(datum.value for datum in self.datums) <= 0:
            raise ValueError("PiePlotData total value must be greater than 0.")

        return self
