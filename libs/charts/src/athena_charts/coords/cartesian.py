from typing import Literal, Self

from pydantic import Field, model_validator

from athena_charts.coords import CartesianAxis, CartesianGridOptions, Coord


class CartesianCoord(Coord):
    kind: Literal["cartesian"] = Field("cartesian", description="笛卡尔坐标系")

    x_axis: CartesianAxis = Field(..., description="X 轴")
    left_y_axis: CartesianAxis | None = Field(None, description="左 Y 轴")
    right_y_axis: CartesianAxis | None = Field(None, description="右 Y 轴")

    grid: CartesianGridOptions = Field(default_factory=CartesianGridOptions.show_none, description="网格配置")

    @model_validator(mode="after")
    def validate_y_axes(self) -> Self:
        if self.left_y_axis is None and self.right_y_axis is None:
            raise ValueError("CartesianCoord must contain at least one Y axis.")

        return self
