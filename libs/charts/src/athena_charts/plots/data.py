
from typing import Any, Self

from athena_core.models import BaseAthenaModel
from pydantic import Field, model_validator


class XYPlotData(BaseAthenaModel):
    x: list[Any] = Field(..., description="X 轴数据")
    y: list[int | float | None] = Field(..., description="Y 轴数据")

    @model_validator(mode="after")
    def validate_lengths(self) -> Self:
        if len(self.x) != len(self.y):
            raise ValueError("XYPlotData.x and XYPlotData.y must have the same length.")
        return self

