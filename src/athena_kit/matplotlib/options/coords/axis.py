from typing import Self

from pydantic import Field, field_serializer

from athena_kit.matplotlib.adapters import to_mpl_line_style
from athena_kit.matplotlib.options._base import _BaseOptions
from athena_kit.matplotlib.types import FontWeight, LineStyle


class AxisSpineOptions(_BaseOptions):
    visible: bool | None = Field(None, description="是否显示坐标轴线")
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
        *,
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
        *,
        labelsize: int | None = None,
        labelweight: FontWeight | None = None,
        labelcolor: str | None = None,
    ):
        return cls(visible=True, labelsize=labelsize, labelweight=labelweight, labelcolor=labelcolor)


class AxisOptions(_BaseOptions):
    spine: AxisSpineOptions | None = Field(None, description="坐标轴线配置项")
    label: AxisLabelOptions | None = Field(None, description="坐标轴标题配置项")

    @classmethod
    def hide_all(cls) -> Self:
        return cls.of(
            spine=AxisSpineOptions.hide(),
            label=AxisLabelOptions.hide(),
        )

    @classmethod
    def hide_spine(
        cls,
        *,
        labelsize: int | None = None,
        labelweight: FontWeight | None = None,
        labelcolor: str | None = None,
    ) -> Self:
        return cls.of(
            spine=AxisSpineOptions.hide(),
            label=AxisLabelOptions.show(labelsize=labelsize, labelweight=labelweight, labelcolor=labelcolor),
        )

    @classmethod
    def hide_label(
        cls,
        *,
        linewidth: float | None = None,
        linecolor: str | None = None,
        linestyle: LineStyle | None = None,
    ) -> Self:
        return cls.of(
            spine=AxisSpineOptions.show(linewidth=linewidth, linecolor=linecolor, linestyle=linestyle),
            label=AxisLabelOptions.hide(),
        )

    @classmethod
    def of(cls, *, spine: AxisSpineOptions | None = None, label: AxisLabelOptions | None = None) -> Self:
        return cls(spine=spine, label=label)
