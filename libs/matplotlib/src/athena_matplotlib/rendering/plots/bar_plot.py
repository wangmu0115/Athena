from dataclasses import dataclass

from athena_core.values.optional import optional_or, safe_getattr
from matplotlib.axes import Axes

from athena_matplotlib.options.bar_plot import BarLayoutOptions, BarPlotOptions
from athena_matplotlib.rendering.color_cycle import ColorCycle
from athena_matplotlib.rendering.render_plan import AlignedBarPlots
from athena_matplotlib.specs.plots.bar import BarPlot


class BarArtist:
    def __init__(self, color_cycle: ColorCycle):
        self._color_cycle = color_cycle
        self._post_init()

    def _post_init(self):
        # self._datalabel_layer = DataLabelLayerArtist()
        pass

    def draw(
        self,
        axes: Axes,
        plotgroup: AlignedBarPlots,
        *,
        options: BarPlotOptions | None,
    ) -> None:
        layout_options = optional_or(safe_getattr(options, "bar_layout"), default=BarLayoutOptions())

        resolved_plots = _resolve_bar_layout(plotgroup, options=layout_options)
        for 


@dataclass
class ResolvedBarPlot:
    plot: BarPlot
    width: float
    x_values: list[object]
    x_positions: list[float]
    y_values: list[float]
    label_y_values: list[float]
    bottom_values: list[float] | None = None
    


def _resolve_bar_layout(plotgroup: AlignedBarPlots, options: BarLayoutOptions) -> list[ResolvedBarPlot]:
    pass


def _resolve_group_layout(
    plotgroup: AlignedBarPlots,
    options: BarLayoutOptions,
):
    """
    plots: list[BarPlot]
    x_values: list[object]
    y_values_list: list[list[object]]
    layout_model: BarLayoutMode
    """
    plot_count = len(plotgroup.plots)
    if plot_count == 0:
        return []

    group_width = options.group_width
    inner_gap = options.inner_gap
    bar_width = (group_width - inner_gap * (plot_count - 1)) / plot_count
    start_offset = -group_width / 2 + bar_width / 2

    resolved_plots: list[ResolvedBarPlot] = []

    for index, plot in enumerate(plotgroup.plots):
        offset = start_offset + index * (bar_width + inner_gap)

        x_positions = [x + offset for x in plotgroup.x_positions]

        items.append(
            ResolvedBarItem(
                plot=plot,
                x_values=x_values,
                y_values=plot.y_values,
                width=bar_width,
                bottom_values=None,
                label_y_values=plot.y_values,
            )
        )

    return items
