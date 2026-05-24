from typing import Self

from pydantic import Field

from athena_charts_matplotlib.styles.base import _BaseStyle
from athena_charts_matplotlib.styles.types import FontWeight, GridAxis, LineStyle, TickDirection


class AxisStyle(_BaseStyle):
    linewidth: float | None = Field(None, gt=0, description="坐标轴线宽")
    linecolor: str | None = Field(None, description="坐标轴线颜色")

    labelsize: int | None = Field(None, gt=0, description="坐标轴标题字号")
    labelweight: FontWeight | None = Field(None, description="坐标轴标题粗细")
    labelcolor: str | None = Field(None, description="坐标轴标题颜色")

    @classmethod
    def default(cls) -> Self:
        return cls.of()

    @classmethod
    def of(
        cls,
        linewidth: float = 0.6,
        linecolor: str = "#333333",
        labelsize: int = 6,
        labelweight: FontWeight = "normal",
        labelcolor: str = "#111111",
    ) -> Self:
        return cls(
            linewidth=linewidth,
            linecolor=linecolor,
            labelsize=labelsize,
            labelweight=labelweight,
            labelcolor=labelcolor,
        )


class GridStyle(_BaseStyle):
    visible: bool | None = Field(None, description="是否显示 Grid")
    grid_axis: GridAxis | None = Field(None, description="网格线应用坐标轴范围")
    linecolor: str | None = Field(None, description="网格线颜色")
    linewidth: float | None = Field(None, gt=0, description="网格线宽度")
    linestyle: LineStyle | None = Field(None, description="网格线样式")
    alpha: float | None = Field(None, ge=0, le=1, description="网格线透明度")

    @classmethod
    def default(cls) -> Self:
        return cls.show()

    @classmethod
    def hide(cls) -> Self:
        return cls(visible=False)

    @classmethod
    def show(
        cls,
        *,
        grid_axis: GridAxis = "both",
        linecolor: str = "#999999",
        linewidth: float = 0.2,
        linestyle: LineStyle = "solid",
        alpha: float = 0.25,
    ) -> Self:
        return cls(
            visible=True,
            grid_axis=grid_axis,
            linecolor=linecolor,
            linewidth=linewidth,
            linestyle=linestyle,
            alpha=alpha,
        )


class TickLineStyle(_BaseStyle):
    linecolor: str | None = Field(None, description="刻度线颜色")
    linewidth: float | None = Field(None, gt=0, description="主刻度线宽度")
    linelength: float | None = Field(None, gt=0, description="主刻度线长度")
    direction: TickDirection | None = Field(None, description="刻度线方向")

    @classmethod
    def default(cls) -> Self:
        return cls.of()

    @classmethod
    def of(
        cls,
        linecolor: str = "#333333",
        linewidth: float = 0.6,
        linelength: float = 2.4,
        direction: TickDirection = "out",
    ) -> Self:
        return cls(linecolor=linecolor, linewidth=linewidth, linelength=linelength, direction=direction)


class TickLabelStyle(_BaseStyle):
    labelsize: int | None = Field(None, gt=0, description="刻度文本字号")
    labelcolor: str | None = Field(None, description="刻度文本颜色")

    @classmethod
    def default(cls) -> Self:
        return cls.of()

    @classmethod
    def of(
        cls,
        labelsize: int = 4,
        labelcolor: str = "#111111",
    ) -> Self:
        return cls(labelsize=labelsize, labelcolor=labelcolor)


class TickVisible(_BaseStyle):
    line: bool | None = Field(None, description="刻度线是否显示")
    label: bool | None = Field(None, description="刻度文本是否显示")

    @classmethod
    def all_visible(cls) -> Self:
        return cls.of(line=True, label=True)

    @classmethod
    def all_hide(cls) -> Self:
        return cls.of(line=False, label=False)

    @classmethod
    def of(cls, line: bool, label: bool) -> Self:
        return cls(line=line, label=label)


class TickStyle(_BaseStyle):
    top: TickVisible | None = Field(None, description="顶部刻度显示配置")
    bottom: TickVisible | None = Field(None, description="底部刻度显示配置")
    left: TickVisible | None = Field(None, description="左侧刻度显示配置")
    right: TickVisible | None = Field(None, description="右侧刻度显示配置")

    line: TickLineStyle | None = Field(None, description="刻度线样式")
    label: TickLabelStyle | None = Field(None, description="刻度文本样式")

    @classmethod
    def default(cls) -> Self:
        return cls.of()

    @classmethod
    def of(
        cls,
        top: TickVisible | None = None,
        bottom: TickVisible | None = None,
        left: TickVisible | None = None,
        right: TickVisible | None = None,
        line: TickLineStyle | None = None,
        label: TickLabelStyle | None = None,
    ) -> Self:
        return cls(
            top=top or TickVisible.all_hide(),
            bottom=bottom or TickVisible.all_visible(),
            left=left or TickVisible.all_visible(),
            right=right or TickVisible.all_hide(),
            line=line or TickLineStyle.default(),
            label=label or TickLabelStyle.default(),
        )
