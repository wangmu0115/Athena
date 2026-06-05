from typing import Self

from pydantic import Field

from athena_kit.matplotlib.styles.base import _BaseStyle
from athena_kit.matplotlib.types import LineStyle, MarkerShape


class LinePlotStyle(_BaseStyle):
    linewidth: float | None = Field(None, gt=0, description="默认线宽")
    linestyle: LineStyle | None = Field(None, description="默认线型")
    marker: MarkerShape | None = Field(None, description="默认 Marker 形状")
    marker_size: int | None = Field(None, description="默认 Marker 大小")
    marker_edgewidth: float | None = Field(None, description="默认 Marker 边框宽度")

    @classmethod
    def of(
        cls,
        linewidth: float = 0.8,
        linestyle: LineStyle = "solid",
        marker: MarkerShape = "circle",
        marker_size: int = 4,
        marker_edgewidth: float = 0.8,
    ) -> Self:
        return cls(
            linewidth=linewidth,
            linestyle=linestyle,
            marker=marker,
            marker_size=marker_size,
            marker_edgewidth=marker_edgewidth,
        )
