import math

from matplotlib.axes import Axes

from athena_core.values.fallbacks import first_not_none
from athena_core.values.optional import optional_map_or, safe_getattr
from athena_matplotlib.options import LinePlotOptions
from athena_matplotlib.options.line_plot import DataLabelOptions
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
        self._draw_data_label(
            axes,
            plot,
            options=safe_getattr(options, "data_label"),
            override=safe_getattr(override, "data_label"),
        )

    def _draw_data_label(
        self,
        axes: Axes,
        plot: AlignedLinePlot,
        *,
        options: DataLabelOptions | None,
        override: DataLabelOptions | None,
    ):
        visible = first_not_none(safe_getattr(override, "visible"), safe_getattr(options, "visible"), default=False)
        if not visible:
            return
        text_params = optional_map_or(options, lambda x: x.build_text_params(), default={})
        text_params.update(optional_map_or(override, lambda x: x.build_text_params(), default={}))

        formatter = first_not_none(
            safe_getattr(override, "formatter"),
            safe_getattr(options, "formatter"),
            default="{y:g}",
        )
        for index, (x, y) in enumerate(zip(plot.x_values, plot.y_values, strict=True)):
            if y is None:
                continue
            if isinstance(y, float) and not math.isfinite(y):
                continue
            text = formatter.format(x=x, y=y, name=plot.plot.name, index=index)
            print(text)
            axes.annotate(
                text,
                xy=(x, y),
                xytext=(0, 6),
                textcoords="offset points",
                zorder=plot.plot.z_index + 1,
                **text_params,
            )

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
