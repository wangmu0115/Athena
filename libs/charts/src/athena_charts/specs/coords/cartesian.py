from typing import Literal, Self

from pydantic import Field, model_validator

from athena_charts.specs.coords.axis import CartesianAxis
from athena_charts.specs.coords.base import Coord
from athena_charts.specs.coords.options import CartesianGridOptions


class CartesianCoord(Coord):
    kind: Literal["cartesian"] = Field("cartesian", description="笛卡尔坐标系")
    x_axis: CartesianAxis = Field(..., description="X 轴")
    left_y_axis: CartesianAxis | None = Field(None, description="左 Y 轴")
    right_y_axis: CartesianAxis | None = Field(None, description="右 Y 轴")
    grid: CartesianGridOptions = Field(default_factory=CartesianGridOptions.show_none, description="网格配置")

    @model_validator(mode="after")
    def validate_axes(self) -> Self:
        if self.x_axis.position not in {"bottom", "top"}:
            raise ValueError("CartesianCoord.x_axis position must be bottom or top.")

        if self.left_y_axis is None and self.right_y_axis is None:
            raise ValueError("CartesianCoord must contain at least one Y axis.")

        if self.left_y_axis is not None and self.left_y_axis.position != "left":
            raise ValueError("left_y_axis position must be left.")

        if self.right_y_axis is not None and self.right_y_axis.position != "right":
            raise ValueError("right_y_axis position must be right.")

        return self

    def get_y_axis(self, side: Literal["left", "right"]) -> CartesianAxis | None:
        if side == "left":
            return self.left_y_axis

        if side == "right":
            return self.right_y_axis

        raise ValueError("CartesianCoord.y_axis position must be left or right.")
