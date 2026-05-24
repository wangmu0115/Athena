from pydoc import resolve

from athena_charts_matplotlib.adapters.axes import resolve_axes_runtime
from matplotlib.axes import Axes

from athena_charts.specs.charts import ChartSpec
from athena_charts_matplotlib.coords._base import _apply_grid
from athena_charts_matplotlib.rendering.options.chart import ChartOptions


class CartesianCoordRenderer:
    def __init__(
        self,
    ):
        pass

    def render(
        self,
        axes: Axes,
        chart: ChartSpec,
        *,
        default_options: ChartOptions | None,
        override_options: ChartOptions | None,
    ):  
        # Axes
        axes_runtime = resolve_axes_runtime(axes, chart.coord)




        # Grid
        _apply_grid(axes, default_options=default_options, override_options=override_options)
        # Axis
        # Plot artists
        axes.twinx()

        # Legend
