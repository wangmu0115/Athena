from typing import Self

from pydantic import Field

from athena_matplotlib.styles.base import _BaseStyle
from athena_matplotlib.types import GridAxis, LineStyle


class GridStyle(_BaseStyle):
    visible: bool | None = Field(None, description="是否显示 Grid")
    grid_axis: GridAxis | None = Field(None, description="网格线应用坐标轴范围")
    linecolor: str | None = Field(None, description="网格线颜色")
    linewidth: float | None = Field(None, gt=0, description="网格线宽度")
    linestyle: LineStyle | None = Field(None, description="网格线样式")
    alpha: float | None = Field(None, ge=0, le=1, description="网格线透明度")

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
