from typing import Self

import matplotlib as mpl
from pydantic import Field

from athena_kit.matplotlib.options._base import _BaseOptions
from athena_kit.matplotlib.options.chart import ChartOptions
from athena_kit.matplotlib.options.coords import CartesianCoordOptions
from athena_kit.matplotlib.options.figure import FigureOptions
from athena_kit.matplotlib.options.plots.bar import BarPlotOptions
from athena_kit.matplotlib.options.plots.line import LinePlotOptions


class RenderFigureOptions(_BaseOptions):
    size: tuple[int, int] | None = Field(None, description="画布大小: (width, height)")
    dpi: int | None = Field(None, gt=0, description="分辨率，每英寸点数")

    figure: FigureOptions | None = Field(None, description="画布样式配置")
    chart: ChartOptions | None = Field(None, description="图表样式配置")
    cartesian: CartesianCoordOptions | None = Field(None, description="笛卡尔坐标系样式配置")

    line_plot: LinePlotOptions | None = Field(None, description="Line Plot 样式配置")
    bar_plot: BarPlotOptions | None = Field(None, description="Bar Plot 样式配置")

    def build_figure_params(self) -> dict[str, object]:
        if self.size is not None:
            dpi = self.dpi or mpl.rcParams["figure.dpi"]
            width, height = self.size
            return {"figsize": (width / dpi, height / dpi), "dpi": dpi}
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
        bar_plot: BarPlotOptions | None = None,
    ) -> Self:
        return cls(
            size=size,
            dpi=dpi,
            figure=figure,
            chart=chart,
            cartesian=cartesian,
            line_plot=line_plot,
            bar_plot=bar_plot,
        )
