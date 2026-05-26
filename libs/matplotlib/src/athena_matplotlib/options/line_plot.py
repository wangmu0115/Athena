from typing import Self

from pydantic import Field, field_serializer

from athena_matplotlib.adapters import to_mpl_line_style
from athena_matplotlib.options._base import _BaseOptions
from athena_matplotlib.types import (
    FontWeight,
    HorizontalAlignment,
    LineStyle,
    MarkerShape,
    VerticalAlignment,
)


class LineOptions(_BaseOptions):
    linewidth: float | None = Field(None, gt=0, description="线宽")
    linestyle: LineStyle | None = Field(None, description="线型")
    linecolor: str | None = Field(None, description="线的颜色", alias="color")

    @field_serializer("linestyle")
    def serialize_linestyle(self, value: LineStyle) -> str:
        return to_mpl_line_style(value)


class MarkerOptions(_BaseOptions):
    marker: MarkerShape | None = Field(None, description="标记形状")
    markersize: float | None = Field(None, gt=0, description="标记大小")
    marker_facecolor: str | None = Field(None, description="标记填充颜色", alias="markerfacecolor")
    marker_edgecolor: str | None = Field(None, description="标记边框颜色", alias="markeredgecolor")
    marker_edgewidth: float | None = Field(None, ge=0, description="标记边框宽度", alias="markeredgewidth")

    @classmethod
    def hide(cls) -> Self:
        return cls(marker=None)

    @classmethod
    def show(
        cls,
        marker: MarkerShape = "circle",
        *,
        markersize: float | None = None,
        marker_facecolor: str | None = None,
        marker_edgecolor: str | None = None,
        marker_edgewidth: float | None = None,
    ):
        return cls(
            marker=marker,
            markersize=markersize,
            marker_facecolor=marker_facecolor,
            marker_edgecolor=marker_edgecolor,
            marker_edgewidth=marker_edgewidth,
        )


class DataLabelOptions(_BaseOptions):
    visible: bool = Field(False, description="是否显示数据标签")
    formatter: str | None = Field(
        None,
        description="标签格式模板，例如 `{y:+g}`、`({x}, {y})`、`{name}: {percent:.1%}`",
    )
    color: str | None = Field(None, description="默认颜色")
    fontsize: int | None = Field(None, gt=0, description="字号")
    fontweight: FontWeight | None = Field(None, description="字体粗细")

    offset_x: float = Field(0, description="标签 X 方向偏移量，单位为 points")
    offset_y: float = Field(6, description="标签 Y 方向偏移量，单位为 points")
    ha: HorizontalAlignment = Field("center", description="水平对齐方式")
    va: VerticalAlignment = Field("bottom", description="垂直对齐方式")

    @classmethod
    def hide(cls) -> Self:
        return cls(visible=False)

    @classmethod
    def show(
        cls,
        formatter: str | None = None,
        *,
        color: str | None = None,
        fontsize: int | None = None,
        fontweight: FontWeight | None = None,
        offset_x: float = 0,
        offset_y: float = 6,
        ha: HorizontalAlignment = "center",
        va: VerticalAlignment = "bottom",
    ):
        return cls(
            visible=True,
            formatter=formatter,
            color=color,
            fontsize=fontsize,
            fontweight=fontweight,
            offset_x=offset_x,
            offset_y=offset_y,
            ha=ha,
            va=va,
        )

    def build_text_params(self) -> dict[str, object]:
        return self.model_dump(
            include=["color", "fontsize", "fontweight", "ha", "va"],
            exclude_none=True,
        )


class LinePlotOptions(_BaseOptions):
    line: LineOptions | None = Field(None, description="线")
    marker: MarkerOptions | None = Field(None, description="标记点")
    data_label: DataLabelOptions | None = Field(None, description="数据标签")

    @classmethod
    def of(
        cls,
        *,
        linewidth: float | None = None,
        linestyle: LineStyle | None = None,
        linecolor: str | None = None,
        marker: MarkerOptions | None = None,
        data_label: DataLabelOptions | None = None,
    ) -> Self:
        line = LineOptions(linewidth=linewidth, linestyle=linestyle, linecolor=linecolor)
        return cls(
            line=line,
            marker=marker,
            data_label=data_label,
        )

    def build_plot_params(self) -> dict[str, object]:
        params: dict[str, object] = {}

        if self.line is not None:
            params.update(self.line.model_dump(exclude_none=True, by_alias=True))
        if self.marker is not None:
            params.update(self.marker.model_dump(exclude_none=True, by_alias=True))

        return params
