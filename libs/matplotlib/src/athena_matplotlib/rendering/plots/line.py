from matplotlib.axes import Axes

from athena_core.values.optional import optional_map_or
from athena_matplotlib.options import LinePlotOptions
from athena_matplotlib.rendering.color_cycle import ColorCycle
from athena_matplotlib.rendering.render_plan import AlignedLinePlot


class LineArtist:
    def __init__(self, color_cycle: ColorCycle):
        self._color_cycle = color_cycle

    def draw(
        self,
        axes: Axes,
        plot: AlignedLinePlot,
        *,
        options: LinePlotOptions | None,
    ) -> None:
        # 绘制折线图
        override = plot.plot.options
        axes.plot(
            plot.x_values,
            plot.y_values,
            zorder=plot.plot.z_index,
            label=plot.plot.name,
            **self._resolve_plot_params(options=options, override=override),
        )
        # 数据标签

    def _resolve_plot_params(
        self,
        *,
        options: LinePlotOptions | None,
        override: LinePlotOptions | None,
    ) -> dict[str, object]:
        params: dict[str, object] = optional_map_or(options, lambda x: x.build_plot_params(), default={})
        if override is not None:
            params.update(optional_map_or(override, lambda x: x.build_plot_params(), default={}))

        if "color" not in params:
            linecolor = self._color_cycle.next()
            if linecolor:
                params["color"] = linecolor

        return params
