from dataclasses import dataclass

from matplotlib.axes import Axes

from athena_core.values.optional import optional_or, safe_getattr
from athena_matplotlib.options.plots.bar import BarLayoutOptions, BarPlotOptions
from athena_matplotlib.rendering.color_cycle import ColorCycle
from athena_matplotlib.rendering.plots.layers.bar_layer import BarLayerArtist
from athena_matplotlib.rendering.coords._render_plan import AlignedBarPlots
from athena_matplotlib.specs.plots.bar import BarPlot


class BarArtist:
    def __init__(self, color_cycle: ColorCycle):
        self._color_cycle = color_cycle
        self._post_init()

    def _post_init(self):
        self._bar_layer = BarLayerArtist(self._color_cycle)
        # self._datalabel_layer = DataLabelLayerArtist()
        pass

    def draw(
        self,
        axes: Axes,
        plotgroup: AlignedBarPlots,
        *,
        options: BarPlotOptions | None = None,
    ) -> None:
        layout_options = optional_or(safe_getattr(options, "layout"), default=BarLayoutOptions.of())
        resolved_plots = _resolve_bar_layout(plotgroup, options=layout_options)
        for resolved_plot in resolved_plots:
            self._bar_layer.draw(
                axes,
                resolved_plot.x_positions,
                resolved_plot.y_values,
                bottom=resolved_plot.bottom_values,
                width=resolved_plot.width,
                plot_name=resolved_plot.plot.name,
                z_index=resolved_plot.plot.z_index,
            )


@dataclass
class ResolvedBarPlot:
    """解析后的柱状图绘制数据，在经过 `X 轴对齐`、`分类排序`、`柱状布局计算`和`坐标位置计算`得到的最终绘制结果。

    Attributes:
        plot: 原始柱状图定义对象。
        width: 当前柱子的实际宽度。
        x_values: 原始 X 轴业务值。
        x_positions: Matplotlib 使用的实际 X 坐标位置，用于真正参与绘图。
        y_values: 柱状图实际绘制的高度值。
        label_y_values: 数据标签 (DataLabel) 使用的 Y 坐标值。
        bottom_values: 柱状图底部偏移值。
    """

    plot: BarPlot
    width: float
    x_values: list[object]
    x_positions: list[float]
    y_values: list[float]
    label_y_values: list[float]
    bottom_values: list[float] | None = None


def _resolve_bar_layout(plotgroup: AlignedBarPlots, *, options: BarLayoutOptions) -> list[ResolvedBarPlot]:
    match plotgroup.layout_mode:
        case "group":
            return _resolve_group_layout(plotgroup, options)
        case "stack":
            return _resolve_stack_layout(plotgroup, options)
        case "overlay":
            return _resolve_overlay_layout(plotgroup, options)
        case _:
            raise ValueError(f"Unsupported bar layout mode: {plotgroup.layout_mode}.")


def _resolve_group_layout(plotgroup: AlignedBarPlots, options: BarLayoutOptions) -> list[ResolvedBarPlot]:
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
        raw_y_values = plotgroup.y_values_list[index]
        y_values = [float(y) if y is not None else 0.0 for y in raw_y_values]
        resolved_plots.append(
            ResolvedBarPlot(
                plot=plot,
                width=bar_width,
                x_values=plotgroup.x_values,
                x_positions=x_positions,
                y_values=y_values,
                label_y_values=y_values,
                bottom_values=None,
            )
        )
    return resolved_plots


def _resolve_stack_layout(plotgroup: AlignedBarPlots, options: BarLayoutOptions) -> list[ResolvedBarPlot]:
    width = options.group_width
    count = len(plotgroup.x_positions)

    positive_bottom = [0.0] * count
    negative_bottom = [0.0] * count

    resolved_plots: list[ResolvedBarPlot] = []
    for index, plot in enumerate(plotgroup.plots):
        raw_y_values = plotgroup.y_values_list[index]
        y_values = [float(y) if y is not None else 0.0 for y in raw_y_values]

        bottom_values: list[float] = []
        label_y_values: list[float] = []

        for i, y in enumerate(y_values):
            if options.separate_positive_negative_stack and y < 0:
                bottom = negative_bottom[i]
                negative_bottom[i] += y
            else:
                bottom = positive_bottom[i]
                positive_bottom[i] += y

            bottom_values.append(bottom)
            label_y_values.append(bottom + y)

        resolved_plots.append(
            ResolvedBarPlot(
                plot=plot,
                width=width,
                x_values=plotgroup.x_values,
                x_positions=plotgroup.x_positions,
                y_values=y_values,
                label_y_values=label_y_values,
                bottom_values=bottom_values,
            )
        )

    return resolved_plots


def _resolve_overlay_layout(plotgroup: AlignedBarPlots, options: BarLayoutOptions) -> list[ResolvedBarPlot]:
    resolved_plots: list[ResolvedBarPlot] = []

    for index, plot in enumerate(plotgroup.plots):
        width = options.group_width * (options.overlay_width_ratio**index)

        y_values = [float(y) if y is not None else 0.0 for y in plotgroup.y_values_list[index]]
        resolved_plots.append(
            ResolvedBarPlot(
                plot=plot,
                width=width,
                x_values=plotgroup.x_values,
                x_positions=plotgroup.x_positions,
                y_values=y_values,
                label_y_values=y_values,
                bottom_values=None,
            )
        )

    return resolved_plots
