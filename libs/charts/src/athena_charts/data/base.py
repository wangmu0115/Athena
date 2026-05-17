from typing import Annotated, Self

from pydantic import Field, model_validator

from athena_charts.data.categorical import CategoricalSeriesData
from athena_charts.data.xy import XYSeriesData
from athena_core.models import BaseAthenaModel


class LinePlotData(BaseAthenaModel):
    data: XYSeriesData = Field(..., description="折线图数据")


type BarPlotDataValue = Annotated[XYSeriesData | CategoricalSeriesData, Field(discriminator="kind")]


class BarPlotData(BaseAthenaModel):
    data: BarPlotDataValue = Field(..., description="柱状图数据")


class PiePlotData(BaseAthenaModel):
    data: CategoricalSeriesData = Field(..., description="饼状图数据")

    @model_validator(mode="after")
    def validate(self) -> Self:
        if any(datum.value is None for datum in self.data.datums):
            raise ValueError("PiePlotData values cannot be None.")

        if any(datum.value < 0 for datum in self.data.datums):
            raise ValueError("PiePlotData values cannot be negative.")

        if sum(datum.value for datum in self.data.datums) <= 0:
            raise ValueError("PiePlotData total value must be greater than 0.")

        return self
