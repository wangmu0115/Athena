from matplotlib.axes import Axes

from athena_charts.specs import ChartSpec
from athena_matplotlib.options.renderfig import RenderFigureOptions


class ChartRenderer:
    def render(self, axes: Axes, chart: ChartSpec, *, options: RenderFigureOptions): ...
