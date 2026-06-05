from matplotlib.axes import Axes

from athena_kit.matplotlib.options.plots.bar import BarOptions
from athena_kit.matplotlib.options.plots.line import LineOptions
from athena_kit.matplotlib.rendering.color_cycle import ColorCycle


class BarLayerArtist:
    def __init__(self, color_cycle: ColorCycle):
        self._color_cycle = color_cycle

    def draw(
        self,
        axes: Axes,
        x_positions: list[float],
        y_values: list[float | None],
        *,
        bottom: list[float] | None,
        width: float,
        plot_name: str = "",
        z_index: int = 100,
        options: BarOptions | None = None,
        override: BarOptions | None = None,
    ):
        # line_params = _build_line_params(self._color_cycle, options=options, override=override)
        axes.bar(
            x_positions,
            y_values,
            width=width,
            bottom=bottom,
            label=plot_name,
            # antialiased=True,
            # marker="none",  # don't draw marker
            # **line_params,
        )


def _build_line_params(
    color_cycle: ColorCycle,
    *,
    options: LineOptions | None = None,
    override: LineOptions | None = None,
) -> dict[str, object]:
    params: dict[str, object] = {}

    if options is not None:
        params.update(options.model_dump(exclude_none=True, by_alias=True))
    if override is not None:
        params.update(override.model_dump(exclude_none=True, by_alias=True))

    if "color" not in params:
        linecolor = color_cycle.next()
        if linecolor:
            params["color"] = linecolor

    return params
