from typing import Literal

from pydantic import Field

from athena_charts.specs.plots.base import Plot


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


class PiePlot(Plot):
    kind: Literal["pie"] = Field("pie", description="饼图")
    coord_kind: Literal["polar"] = Field("polar", description="极坐标系")
    data: PiePlotData = Field(..., description="饼图数据")
