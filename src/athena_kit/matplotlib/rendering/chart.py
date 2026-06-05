from matplotlib.axes import Axes

from athena_kit.matplotlib.decorations import apply_chart_style
from athena_kit.matplotlib.options import RenderFigureOptions
from athena_kit.matplotlib.rendering.color_cycle import ColorCycle
from athena_kit.matplotlib.rendering.coords import CartesianCoordRenderer
from athena_kit.matplotlib.specs import ChartSpec
from athena_kit.matplotlib.specs.coords import CartesianCoord


class ChartRenderer:
    def __init__(self, color_cycle: ColorCycle):
        self._cartesian_renderer = CartesianCoordRenderer(color_cycle)

    def render(self, axes: Axes, chart: ChartSpec, *, options: RenderFigureOptions):
        # 图表背景色和图表标题
        apply_chart_style(axes, chart, options=options.chart)
        # 坐标系系统
        if isinstance(chart.coord, CartesianCoord):  # 笛卡尔直角坐标系
            self._cartesian_renderer.render(axes, chart, options=options)
        # elif isinstance(chart.coord, PolarCoord): # 极坐标系
