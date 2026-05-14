from typing import Self

from pydantic import Field

from athena_core.models import BaseAthenaModel


class CartesianGridOptions(BaseAthenaModel):
    visible: bool = Field(True, description="是否显示网格")
    x: bool = Field(True, description="是否显示 X 方向网格")
    y: bool = Field(True, description="是否显示 Y 方向网格")
    alpha: float = Field(0.25, ge=0, le=1, description="网格透明度")

    @classmethod
    def show_none(cls) -> Self:
        return Self(visible=False)

    @classmethod
    def show_x(cls, alpha: float = 0.25) -> Self:
        return Self(visible=True, x=True, y=False, alpha=alpha)

    @classmethod
    def show_y(cls, alpha: float = 0.25) -> Self:
        return Self(visible=True, x=False, y=True, alpha=alpha)

    @classmethod
    def show_both(cls, alpha: float = 0.25) -> Self:
        return Self(visible=True, x=True, y=True, alpha=alpha)
