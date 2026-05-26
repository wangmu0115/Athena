from dataclasses import dataclass
from typing import Literal, Self

from pydantic import Field, model_validator

from athena_matplotlib.options import CartesianCoordOptions
from athena_matplotlib.specs.coords.base import AxisSpec, Coord
from athena_matplotlib.specs.coords.tick import TickSpec
from athena_matplotlib.types import AxisDataType, AxisScale, CartesianAxisPosition


class CartesianAxisSpec(AxisSpec):
    position: CartesianAxisPosition = Field(..., description="坐标轴位置")

    @classmethod
    def x_axis(
        cls,
        position: Literal["bottom", "top"] = "bottom",
        data_type: AxisDataType = "category",
        tick: TickSpec | None = None,
        *,
        label: str = "",
        scale: AxisScale = "linear",
        min: object | None = None,
        max: object | None = None,
    ):
        return cls(
            position=position,
            label=label,
            data_type=data_type,
            scale=scale,
            min=min,
            max=max,
            tick=tick,
        )

    @classmethod
    def y_axis(
        cls,
        position: Literal["left", "right"] = "left",
        tick: TickSpec | None = None,
        *,
        label: str = "",
        scale: AxisScale = "linear",
        min: object | None = None,
        max: object | None = None,
    ):
        return cls(
            position=position,
            label=label,
            data_type="number",
            scale=scale,
            min=min,
            max=max,
            tick=tick,
        )

    @model_validator(mode="after")
    def validate(self) -> Self:
        if self.position in {"left", "right"} and self.data_type != "number":
            raise ValueError("Cartesian Y axis must use number data_type.")
        return self


class CartesianCoord(Coord):
    """笛卡尔坐标系规范，用于描述直角坐标系中的 X 轴、Y 轴与网格配置。

    约束：
        - 只支持单 X 轴，可以位于 `bottom` 或 `top`。
        - 左 Y 轴和右 Y 轴至少存在一个。
    """

    kind: Literal["cartesian"] = Field("cartesian", description="笛卡尔坐标系")
    x_axis: CartesianAxisSpec = Field(..., description="主 X 轴，位于 bottom 位置")
    left_y_axis: CartesianAxisSpec | None = Field(None, description="左 Y 轴")
    right_y_axis: CartesianAxisSpec | None = Field(None, description="右 Y 轴")

    options: CartesianCoordOptions | None = Field(None, description="运行时样式配置")

    @dataclass
    def of(
        cls,
        x_axis: CartesianAxisSpec,
        *,
        left_y_axis: CartesianAxisSpec | None = None,
        right_y_axis: CartesianAxisSpec | None = None,
        options: CartesianCoordOptions | None = None,
    ) -> Self:
        return cls(
            kind="cartesian",
            x_axis=x_axis,
            left_y_axis=left_y_axis,
            right_y_axis=right_y_axis,
            options=options,
        )

    @model_validator(mode="after")
    def validate(self) -> Self:
        if self.left_y_axis is None and self.right_y_axis is None:
            raise ValueError("Cartesian coord must contain at least one Y axis.")
        if self.left_y_axis is not None and self.left_y_axis.position != "left":
            raise ValueError("Cartesian left y_axis must be at left position.")
        if self.right_y_axis is not None and self.right_y_axis.position != "right":
            raise ValueError("Cartesian right y_axis must be at left position.")

        return self

    def get_x_axis(self, side: Literal["bottom", "top"]) -> CartesianAxisSpec | None:
        if self.x_axis.position == side:
            return self.x_axis
        return None

    def get_y_axis(self, side: Literal["left", "right"]) -> CartesianAxisSpec | None:
        if side == "left":
            return self.left_y_axis
        if side == "right":
            return self.right_y_axis
        raise ValueError("Cartesian y_axis position must be left or right.")
