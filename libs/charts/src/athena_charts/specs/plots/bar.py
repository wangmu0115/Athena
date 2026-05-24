from typing import Annotated, Literal, Self

from pydantic import Field

from athena_charts.specs.coords import Coord
from athena_charts.specs.plots.base import Plot
from athena_charts.specs.plots.datas import CategoricalSeriesData, XYSeriesData

type BarPlotData = Annotated[XYSeriesData | CategoricalSeriesData, Field(discriminator="kind")]


class BarPlot(Plot):
    kind: Literal["bar"] = Field("bar", description="柱状图")
    coord_kind: Literal["cartesian"] = Field("cartesian", description="笛卡尔坐标系")
    x_axis_side: Literal["bottom", "top"] = Field("bottom", description="使用底部 X 轴或顶部 X 轴")
    y_axis_side: Literal["left", "right"] = Field("left", description="使用左侧或右侧 Y 轴")
    data: BarPlotData = Field(..., description="图层数据")

    @classmethod
    def of(
        cls,
        x_axis_side: Literal["bottom", "top"] = "bottom",
        y_axis_side: Literal["left", "right"] = "left",
        *,
        name: str = "",
        z_index: int = 90,
        data: BarPlotData,
    ) -> Self:
        return cls(
            name=name,
            z_index=z_index,
            kind="bar",
            coord_kind="cartesian",
            x_axis_side=x_axis_side,
            y_axis_side=y_axis_side,
            data=data,
        )

    def validate_coord(self, coord: Coord):
        super().validate_coord(coord)
        if self.x_axis_side != coord.x_axis.position:
            raise ValueError(f"Plot {self.name or self.kind} use {self.x_axis_side} X axis, but coord doesn't define it.")
        if coord.get_y_axis(self.y_axis_side) is None:
            raise ValueError(f"Plot {self.name or self.kind} use {self.y_axis_side} Y axis, but coord does not define it.")
