from typing import Self

from pydantic import Field

import matplotlib as mpl
from athena_matplotlib.options._base import _BaseOptions
from athena_matplotlib.options.figure import FigureOptions


class RenderFigureOptions(_BaseOptions):
    size: tuple[int, int] | None = Field(None, description="画布大小: (width, height)")
    dpi: int | None = Field(None, gt=0, description="分辨率，每英寸点数")

    figure: FigureOptions | None = Field(None, description="画布样式配置")

    def build_figure_params(self) -> dict[str, object]:
        if self.size is not None:
            dpi = self.dpi or mpl.rcParams["figure.dpi"]
            figsize = self.size / dpi
            return {"figsize": figsize, "dpi": dpi}
        return {}

    @classmethod
    def default(cls):
        """所有运行时配置项都为 `None`"""
        return cls.of()

    @classmethod
    def of(
        cls,
        size: tuple[int, int] | None = None,
        dpi: int | None = None,
        figure: FigureOptions | None = None,
    ) -> Self:
        return cls(
            size=size,
            dpi=dpi,
            figure=figure,
        )
