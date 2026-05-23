from typing import Self

from pydantic import Field

from athena_charts_matplotlib.rendering.options.base import ColorCycle, _BaseOptions
from athena_charts_matplotlib.rendering.options.figure import FigureOptions
from athena_charts_matplotlib.rendering.options.savefig import SaveFigureOptions


class MatplotlibRenderOptions(_BaseOptions):
    figure: FigureOptions | None = Field(None, description="画布运行时配置项")

    color_cycle: ColorCycle | None
    save_figure: SaveFigureOptions | None = Field(None, description="保持图像的配置项")

    @classmethod
    def default(cls, colors: list[str] | None = None) -> Self:
        return cls.of(
            color_cycle=ColorCycle(colors),
        )

    @classmethod
    def of(
        cls,
        figure: FigureOptions | None = None,
        color_cycle: ColorCycle | None = None,
        save_figure: SaveFigureOptions | None = None,
    ) -> Self:
        return cls(
            figure=figure,
            color_cycle=color_cycle,
            save_figure=save_figure or SaveFigureOptions.png(),
        )
