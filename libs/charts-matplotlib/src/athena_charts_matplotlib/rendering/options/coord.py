from typing import Self

from pydantic import Field, field_serializer

from athena_charts_matplotlib.adapters.styles import to_mpl_line_style
from athena_charts_matplotlib.rendering.options.base import _BaseOptions
from athena_charts_matplotlib.styles import FontWeight, GridAxis, LineStyle, TickDirection


class GridOptions(_BaseOptions):
    visible: bool | None = Field(None, description="是否显示 Grid")
    grid_axis: GridAxis | None = Field(None, description="网格线应用坐标轴范围", alias="axis")
    linecolor: str | None = Field(None, description="网格线颜色", alias="color")
    linewidth: float | None = Field(None, gt=0, description="网格线宽度")
    linestyle: LineStyle | None = Field(None, description="网格线样式")
    alpha: float | None = Field(None, ge=0, le=1, description="网格线透明度")

    @field_serializer("linestyle")
    def serialize_linestyle(self, value: LineStyle) -> str:
        return to_mpl_line_style(value)

    def build_grid_params(self) -> dict[str, object]:
        return self.model_dump(exclude_none=True, by_alias=True, exclude=["visible"])

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
        grid_axis: GridAxis | None = None,
        linecolor: str | None = None,
        linewidth: float | None = None,
        linestyle: LineStyle | None = None,
        alpha: float | None = None,
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
    linestyle: LineStyle | None = Field(None, description="坐标轴线样式")

    @field_serializer("linestyle")
    def serialize_linestyle(self, value: LineStyle) -> str:
        return to_mpl_line_style(value)

    @classmethod
    def hide(cls) -> Self:
        return cls(visible=False)

    @classmethod
    def show(
        cls,
        linewidth: float | None = None,
        linecolor: str | None = None,
        linestyle: LineStyle | None = None,
    ):
        return cls(visible=True, linewidth=linewidth, linecolor=linecolor, linestyle=linestyle)


class AxisLabelOptions(_BaseOptions):
    visible: bool | None = Field(None, description="是否显示坐标轴标题")
    labelsize: int | None = Field(None, gt=0, description="坐标轴标题字号", alias="fontsize")
    labelweight: FontWeight | None = Field(None, description="坐标轴标题粗细", alias="fontweight")
    labelcolor: str | None = Field(None, description="坐标轴标题颜色", alias="color")

    @classmethod
    def hide(cls) -> Self:
        return cls(visible=False)

    @classmethod
    def show(
        cls,
        labelsize: int | None = None,
        labelweight: FontWeight | None = None,
        labelcolor: str | None = None,
    ):
        return cls(visible=True, labelsize=labelsize, labelweight=labelweight, labelcolor=labelcolor)


class AxisOptions(_BaseOptions):
    spine: AxisSpineOptions | None = Field(None, description="坐标轴线配置项")
    label: AxisLabelOptions | None = Field(None, description="坐标轴标题配置项")

    def build_spine_params(self) -> dict[str, object]:
        if self.spine is None:
            return {}
        return self.spine.model_dump(exclude_none=True, by_alias=True)

    def build_label_params(self) -> dict[str, object]:
        if self.label is None:
            return {}
        return self.label.model_dump(exclude_none=True, by_alias=True)


class TickLineOptions(_BaseOptions):
    visible: bool | None = Field(None, description="是否显示刻度线")
    linecolor: str | None = Field(None, description="刻度线颜色", alias="color")
    linewidth: float | None = Field(None, gt=0, description="主刻度线宽度", alias="width")
    linelength: float | None = Field(None, gt=0, description="主刻度线长度", alias="length")
    direction: TickDirection | None = Field(None, description="刻度线方向")

    @classmethod
    def hide(cls) -> Self:
        return cls(visible=False)

    @classmethod
    def show(
        cls,
        linecolor: str | None = None,
        linewidth: float | None = None,
        linelength: float | None = None,
        direction: TickDirection | None = None,
    ):
        return cls(visible=True, linecolor=linecolor, linewidth=linewidth, linelength=linelength, direction=direction)


class TickLabelOptions(_BaseOptions):
    visible: bool | None = Field(None, description="是否显示刻度文本")
    labelsize: int | None = Field(None, gt=0, description="刻度文本字号")
    labelcolor: str | None = Field(None, description="刻度文本颜色")
    rotation: float | None = Field(None, ge=-90, le=90, description="刻度文本旋转角度")

    @classmethod
    def hide(cls) -> Self:
        return cls(visible=False)

    @classmethod
    def show(
        cls,
        labelsize: int | None = None,
        labelcolor: str | None = None,
        rotation: float | None = None,
    ):
        return cls(visible=True, labelsize=labelsize, labelcolor=labelcolor, rotation=rotation)


class TickOptions(_BaseOptions):
    line: TickLineOptions | None = Field(None, description="刻度线配置项")
    label: TickLabelOptions | None = Field(None, description="刻度文本配置项")

    def build_line_params(self) -> dict[str, object]:
        if self.line is None:
            return {}
        return self.line.model_dump(exclude_none=True, by_alias=True)

    def build_label_params(self) -> dict[str, object]:
        if self.label is None:
            return {}
        return self.label.model_dump(exclude_none=True, by_alias=True)


class CoordOptions(_BaseOptions):
    top_axis: AxisOptions | None = Field(None, description="Top X 轴轴线和标题配置项")
    bottom_axis: AxisOptions | None = Field(None, description="Bottom X 轴轴线和标题配置项")
    left_axis: AxisOptions | None = Field(None, description="Left Y 轴轴线和标题配置项")
    right_axis: AxisOptions | None = Field(None, description="Right Y 轴轴线和标题配置项")

    top_tick: TickOptions | None = Field(None, description="Top X 轴刻度线配置项")
    bottom_tick: TickOptions | None = Field(None, description="Bottom X 轴刻度线配置项")
    left_tick: TickOptions | None = Field(None, description="Left Y 轴刻度线配置项")
    right_tick: TickOptions | None = Field(None, description="Right Y 轴刻度线配置项")
