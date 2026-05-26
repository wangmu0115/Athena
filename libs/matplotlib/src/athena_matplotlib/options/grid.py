from typing import Self

from pydantic import Field, field_serializer

from athena_matplotlib.adapters import to_mpl_line_style
from athena_matplotlib.options._base import _BaseOptions
from athena_matplotlib.types import GridAxis, LineStyle


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
