from typing import Self

from pydantic import Field

from athena_kit.matplotlib.styles.base import _BaseStyle
from athena_kit.matplotlib.types import TickDirection


class TickLineStyle(_BaseStyle):
    linecolor: str | None = Field(None, description="刻度线颜色")
    linewidth: float | None = Field(None, gt=0, description="主刻度线宽度")
    linelength: float | None = Field(None, gt=0, description="主刻度线长度")
    direction: TickDirection | None = Field(None, description="刻度线方向")

    @classmethod
    def of(
        cls,
        linecolor: str = "#333333",
        linewidth: float = 0.6,
        linelength: float = 2.4,
        direction: TickDirection = "out",
    ) -> Self:
        return cls(
            linecolor=linecolor,
            linewidth=linewidth,
            linelength=linelength,
            direction=direction,
        )


class TickLabelStyle(_BaseStyle):
    labelsize: int | None = Field(None, gt=0, description="刻度文本字号")
    labelcolor: str | None = Field(None, description="刻度文本颜色")

    @classmethod
    def of(
        cls,
        labelsize: int = 4,
        labelcolor: str = "#111111",
    ) -> Self:
        return cls(labelsize=labelsize, labelcolor=labelcolor)


class TickStyle(_BaseStyle):
    line_visible: tuple[bool, bool, bool, bool] | None = Field(
        None,
        description="[top, bottom, left, right] 坐标轴刻度线是否显示",
    )
    label_visible: tuple[bool, bool, bool, bool] | None = Field(
        None,
        description="[top, bottom, left, right] 坐标轴刻度文本是否显示",
    )
    line: TickLineStyle | None = Field(None, description="刻度线样式")
    label: TickLabelStyle | None = Field(None, description="刻度文本样式")

    @classmethod
    def of(
        cls,
        line_visible: tuple[bool, bool, bool, bool] | None = None,
        label_visible: tuple[bool, bool, bool, bool] | None = None,
        line: TickLineStyle | None = None,
        label: TickLabelStyle | None = None,
    ) -> Self:
        return cls(
            line_visible=line_visible or [False, True, True, False],  # top 和 right 隐藏，bottom 和 left 显式。
            label_visible=label_visible or [False, True, True, False],  # top 和 right 隐藏，bottom 和 left 显式。
            line=line or TickLineStyle.of(),
            label=label or TickLabelStyle.of(),
        )
