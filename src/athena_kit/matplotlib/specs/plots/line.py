from typing import Literal, Self

from pydantic import Field

from athena_kit.matplotlib.datas import XYSeriesData
from athena_kit.matplotlib.options.plots import LinePlotOptions
from athena_kit.matplotlib.specs.coords import Coord
from athena_kit.matplotlib.specs.plots.base import Plot


class LinePlot(Plot):
    kind: Literal["line"] = Field("line", description="折线图")
    coord_kind: Literal["cartesian"] = Field("cartesian", description="笛卡尔坐标系")
    x_axis_side: Literal["bottom", "top"] = Field("bottom", description="使用底部 X 轴或顶部 X 轴")
    y_axis_side: Literal["left", "right"] = Field("left", description="使用左侧或右侧 Y 轴")
    data: XYSeriesData = Field(..., description="折线图数据")

    options: LinePlotOptions | None = Field(None, description="折线图运行时配置项")

    @classmethod
    def of(
        cls,
        data: XYSeriesData,
        x_axis_side: Literal["bottom", "top"] = "bottom",
        y_axis_side: Literal["left", "right"] = "left",
        *,
        name: str = "",
        z_index: int = 100,
        options: LinePlotOptions | None = None,
    ) -> Self:
        return cls(
            kind="line",
            coord_kind="cartesian",
            name=name,
            data=data,
            x_axis_side=x_axis_side,
            y_axis_side=y_axis_side,
            z_index=z_index,
            options=options,
        )

    def validate_coord(self, coord: Coord):
        super().validate_coord(coord)
        if coord.get_x_axis(self.x_axis_side) is None:
            raise ValueError(
                f"Plot {self.name or self.kind} use {self.x_axis_side} X axis, but coord doesn't define it."
            )
        if coord.get_y_axis(self.y_axis_side) is None:
            raise ValueError(
                f"Plot {self.name or self.kind} use {self.y_axis_side} Y axis, but coord doesn't define it."
            )
