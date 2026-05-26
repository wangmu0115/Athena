from typing import Self

from pydantic import Field

import matplotlib as mpl
from athena_matplotlib.options._base import _BaseOptions
from athena_matplotlib.options.cartesian import CartesianCoordOptions
from athena_matplotlib.options.chart import ChartOptions
from athena_matplotlib.options.figure import FigureOptions
from athena_matplotlib.options.line_plot import LinePlotOptions


class RenderFigureOptions(_BaseOptions):
    size: tuple[int, int] | None = Field(None, description="画布大小: (width, height)")
    dpi: int | None = Field(None, gt=0, description="分辨率，每英寸点数")

    figure: FigureOptions | None = Field(None, description="画布样式配置")
    chart: ChartOptions | None = Field(None, description="图表样式配置")
    cartesian: CartesianCoordOptions | None = Field(None, description="笛卡尔坐标系样式配置")
    line_plot: LinePlotOptions | None = Field(None, description="Line Plot 样式配置")

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
        *,
        figure: FigureOptions | None = None,
        chart: ChartOptions | None = None,
        cartesian: CartesianCoordOptions | None = None,
        line_plot: LinePlotOptions | None = None,
    ) -> Self:
        return cls(
            size=size,
            dpi=dpi,
            figure=figure,
            chart=chart,
            cartesian=cartesian,
            line_plot=line_plot,
        )
