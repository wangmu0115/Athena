from typing import Self

from pydantic import Field

from athena_charts.themes import LineStyle
from athena_charts_matplotlib.styles._base import _BaseStyle
from athena_charts_matplotlib.styles.types import GridAxis


class MatplotlibGridStyle(_BaseStyle):
    visible: bool | None = Field(None, description="是否显示 Grid")
    grid_axis: GridAxis | None = Field(None, description="网格线应用坐标轴范围")
    line_color: str | None = Field(None, description="网格线颜色")
    line_width: float | None = Field(None, gt=0, description="网格线宽度")
    line_style: LineStyle | None = Field(None, description="网格线样式")
    alpha: float | None = Field(None, ge=0, le=1, description="网格线透明度")

    @classmethod
    def hide(cls) -> Self:
        return cls(visible=False)

    @classmethod
    def show(
        cls,
        *,
        grid_axis: GridAxis = "both",
        line_color: str = "#999999",
        line_width: float = 0.2,
        line_style: LineStyle = "solid",
        alpha: float = 0.25,
    ) -> Self:
        return cls(
            visible=True,
            grid_axis=grid_axis,
            line_color=line_color,
            line_width=line_width,
            line_style=line_style,
            alpha=alpha,
        )
