from typing import Literal, Self

from pydantic import Field, model_validator

from athena_charts.specs._base import _BaseOptions
from athena_charts.specs.coords.axis import AxisOptions, AxisSpec
from athena_charts.specs.coords.base import Coord
from athena_charts.specs.coords.types import AxisDataType, CartesianAxisPosition


class CartesianAxisSpec(AxisSpec):
    position: CartesianAxisPosition = Field(..., description="坐标轴位置")

    @classmethod
    def primary_x_axis(
        cls,
        *,
        label: str = "",
        data_type: AxisDataType = "category",
        options: AxisOptions | None = None,
    ):
        return cls(
            label=label,
            data_type=data_type,
            position="bottom",
            options=options if options is not None else AxisOptions(),
        )

    @classmethod
    def secondary_x_axis(
        cls,
        *,
        label: str = "",
        data_type: AxisDataType = "category",
        options: AxisOptions | None = None,
    ):
        return cls(
            label=label,
            data_type=data_type,
            position="top",
            options=options if options is not None else AxisOptions(),
        )

    @classmethod
    def left_y_axis(cls, *, label: str = "", options: AxisOptions | None = None):
        return cls(
            label=label,
            data_type="number",
            position="left",
            options=options if options is not None else AxisOptions(),
        )

    @classmethod
    def right_y_axis(cls, *, label: str = "", options: AxisOptions | None = None):
        return cls(
            label=label,
            data_type="number",
            position="right",
            options=options if options is not None else AxisOptions(),
        )

    @model_validator(mode="after")
    def validate(self) -> Self:
        if self.position in {"left", "right"} and self.data_type != "number":
            raise ValueError("Cartesian Y axis must use number data_type.")
        return self


class CartesianGridOptions(_BaseOptions):
    visible: bool | None = Field(None, description="是否显示网格")
    x_visible: bool | None = Field(None, description="是否显示沿 X 轴刻度生成的网格线")
    y_visible: bool | None = Field(None, description="是否显示沿 Y 轴刻度生成的网格线")
    alpha: float | None = Field(None, ge=0, le=1, description="网格透明度")

    @classmethod
    def show_none(cls) -> Self:
        """创建隐藏全部网格线的配置。"""
        return cls(visible=False)

    @classmethod
    def show_x(cls, alpha: float = 0.25) -> Self:
        """创建仅显示 X 方向网格线的配置。"""
        return cls(visible=True, x=True, y=False, alpha=alpha)

    @classmethod
    def show_y(cls, alpha: float = 0.25) -> Self:
        """创建仅显示 Y 方向网格线的配置。"""
        return cls(visible=True, x=False, y=True, alpha=alpha)

    @classmethod
    def show_both(cls, alpha: float = 0.25) -> Self:
        """创建同时显示 X/Y 方向网格线的配置。"""
        return cls(visible=True, x=True, y=True, alpha=alpha)


class CartesianCoord(Coord):
    """笛卡尔坐标系规范，用于描述直角坐标系中的 X 轴、Y 轴与网格配置。

    约束：
        - 主 X 轴必须位于 `bottom`。
        - 辅助 X 轴如果存在，必须位于 `top`。
        - 左 Y 轴和右 Y 轴至少存在一个。
    """

    kind: Literal["cartesian"] = Field("cartesian", description="笛卡尔坐标系")
    x_axis: CartesianAxisSpec = Field(..., description="主 X 轴，位于 bottom 位置")
    secondary_x_axis: CartesianAxisSpec | None = Field(None, description="辅助 X 轴，必须位于 top 位置")
    left_y_axis: CartesianAxisSpec | None = Field(None, description="左 Y 轴")
    right_y_axis: CartesianAxisSpec | None = Field(None, description="右 Y 轴")
    grid: CartesianGridOptions = Field(default_factory=CartesianGridOptions.show_none, description="网格配置")

    @model_validator(mode="after")
    def validate(self) -> Self:
        if self.x_axis.position != "bottom":
            raise ValueError("Cartesian primary x_axis must be at bottom position.")
        if self.secondary_x_axis is not None and self.secondary_x_axis.position != "top":
            raise ValueError("Cartesian secondary x_axis must be at top position.")

        if self.left_y_axis is None and self.right_y_axis is None:
            raise ValueError("Cartesian coord must contain at least one Y axis.")
        if self.left_y_axis is not None and self.left_y_axis.position != "left":
            raise ValueError("Cartesian left y_axis must be at left position.")
        if self.right_y_axis is not None and self.right_y_axis.position != "right":
            raise ValueError("Cartesian right y_axis must be at left position.")

        return self

    def get_y_axis(self, side: Literal["left", "right"]) -> CartesianAxisSpec | None:
        if side == "left":
            return self.left_y_axis
        if side == "right":
            return self.right_y_axis
        raise ValueError("Cartesian y_axis position must be left or right.")
