from typing import Self

from pydantic import Field

from athena_charts_matplotlib.rendering.options.base import _BaseOptions
from athena_charts_matplotlib.styles import FontWeight, GridAxis, LineStyle, TickDirection


class GridOptions(_BaseOptions):
    visible: bool | None = Field(None, description="是否显示 Grid")
    grid_axis: GridAxis | None = Field(None, description="网格线应用坐标轴范围", alias="axis")
    linecolor: str | None = Field(None, description="网格线颜色", alias="color")
    linewidth: float | None = Field(None, gt=0, description="网格线宽度")
    linestyle: LineStyle | None = Field(None, description="网格线样式")
    alpha: float | None = Field(None, ge=0, le=1, description="网格线透明度")

    @classmethod
    def nature(cls, grid_axis: GridAxis = "both") -> Self:
        return cls.show(
            grid_axis=grid_axis,
            linecolor="#E5E5E5",
            linewidth=0.8,
            linestyle="solid",
            alpha=0.8,
        )

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


class AxisSpineOptions(_BaseOptions):
    visible: bool | None = Field(None, description="是否显示坐标轴")
    linewidth: float | None = Field(None, gt=0, description="坐标轴线宽")
    linecolor: str | None = Field(None, description="坐标轴线颜色", alias="color")


class AxisLabelOptions(_BaseOptions):
    visible: bool | None = Field(None, description="是否显示坐标轴标题")
    fontsize: int | None = Field(None, gt=0, description="坐标轴标题字号")
    fontweight: FontWeight | None = Field(None, description="坐标轴标题粗细")
    color: str | None = Field(None, description="坐标轴标题颜色")


class AxisOptions(_BaseOptions):
    spine: AxisSpineOptions | None
    label: AxisLabelOptions | None

    def build_spine_params(self) -> dict[str, object]:
        params: dict[str, object] = {}
        if self.linewidth:
            params["linewidth"] = self.linewidth
        if self.linecolor:
            params["color"] = self.linecolor
        return params


class TickOptions(_BaseOptions):
    line: bool | None = Field(None, description="刻度线是否显示")
    label: bool | None = Field(None, description="刻度文本是否显示")

    linecolor: str | None = Field(None, description="刻度线颜色")
    linewidth: float | None = Field(None, gt=0, description="主刻度线宽度")
    linelength: float | None = Field(None, gt=0, description="主刻度线长度")
    direction: TickDirection | None = Field(None, description="刻度线方向")
    labelsize: int | None = Field(None, gt=0, description="刻度文本字号")
    labelcolor: str | None = Field(None, description="刻度文本颜色")
    lableweight: FontWeight | None = Field(None, description="刻度文本字体粗细")
    rotation: float | None = Field(None, ge=-90, le=90, description="刻度文本旋转角度")


class AxesOptions(_BaseOptions):
    top_x_axis: AxisOptions | None
    top_x_tick: TickOptions | None
    bottom_x_axis: AxisOptions | None
    bottom_x_tick: TickOptions | None

    left_y_axis: AxisOptions | None
    left_y_tick: TickOptions | None
    right_y_axis: AxisOptions | None
    right_y_tick: TickOptions | None
