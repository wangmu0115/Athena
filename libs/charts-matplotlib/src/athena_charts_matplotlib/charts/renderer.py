from matplotlib.axes import Axes

from athena_charts.specs.charts.chart import ChartSpec
from athena_charts_matplotlib.themes.context import MatplotlibRenderContext


class MatplotlibChartRenderer:
    def __init__(
        self,
    ):
        pass

    def render(self, axes: Axes, chart: ChartSpec, *, context: MatplotlibRenderContext) -> None:
        pass
