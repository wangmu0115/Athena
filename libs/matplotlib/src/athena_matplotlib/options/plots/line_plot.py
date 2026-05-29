from typing import Self

from pydantic import Field, field_serializer

from athena_matplotlib.adapters import to_mpl_line_style
from athena_matplotlib.options._base import _BaseOptions
from athena_matplotlib.options.plots.data_label import DataLabelOptions
from athena_matplotlib.options.plots.marker import MarkerOptions
from athena_matplotlib.types import LineStyle


class LineOptions(_BaseOptions):
    linewidth: float | None = Field(None, gt=0, description="线宽")
    linestyle: LineStyle | None = Field(None, description="线型")
    linecolor: str | None = Field(None, description="线的颜色", alias="color")

    @field_serializer("linestyle")
    def serialize_linestyle(self, value: LineStyle) -> str:
        return to_mpl_line_style(value)


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
