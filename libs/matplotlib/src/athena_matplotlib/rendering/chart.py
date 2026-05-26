from matplotlib.axes import Axes

from athena_charts.specs.coords.cartesian import CartesianCoord
from athena_matplotlib.decorations import apply_chart_style
from athena_matplotlib.options import RenderFigureOptions
from athena_matplotlib.rendering.base import ColorCycle
from athena_matplotlib.rendering.coords import CartesianCoordRenderer
from athena_matplotlib.specs import ChartSpec


class ChartRenderer:
    def __init__(self, color_cycle: ColorCycle):
        self._cartesian_renderer = CartesianCoordRenderer(color_cycle)

    def render(self, axes: Axes, chart: ChartSpec, *, options: RenderFigureOptions):
        # 渲染图表样式
        apply_chart_style(axes, chart, options=options.chart)
        # 渲染坐标轴系统
        if isinstance(chart.coord, CartesianCoord):
            self._cartesian_renderer.render(axes, chart, options=options)
