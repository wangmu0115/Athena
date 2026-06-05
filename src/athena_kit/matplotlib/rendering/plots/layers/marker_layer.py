import math

import matplotlib as mpl
from matplotlib.axes import Axes

from athena_kit.matplotlib.adapters.styles import to_mpl_marker_shape
from athena_kit.matplotlib.options.plots.line import MarkerOptions
from athena_kit.matplotlib.options.plots.marker import MarkerStyle, MarkerStyleRule
from athena_kit.matplotlib.options.rules.data_context import DataContext
from athena_kit.matplotlib.options.rules.matches import match_data_condition


class MarkerLayerArtist:
    def draw(
        self,
        axes: Axes,
        x_positions: list[float],
        y_values: list[float | None],
        *,
        semantic_x_values: list[object] | None = None,
        plot_name: str = "",
        z_index: int = 999,
        options: MarkerOptions | None = None,
        override: MarkerOptions | None = None,
    ):
        if options is None and override is None and not mpl.rcParams["lines.marker"]:
            return

        semantic_x_values = semantic_x_values or x_positions

        base_style = _resolve_marker_base_style(options, override)
        style_rules = [
            *(options.rules if options is not None else []),
            *(override.rules if override is not None else []),
        ]
        count = len(x_positions)
        for index, (x_pos, x_raw, y) in enumerate(zip(x_positions, semantic_x_values, y_values, strict=True)):
            if y is None:
                continue
            if isinstance(y, float) and not math.isfinite(y):
                continue

            data_context = DataContext.of(x=x_raw, y=y, index=index, count=count, name=plot_name)
            style = _resolve_marker_style(base_style, style_rules, data_context)
            if not style.marker:
                continue

            axes.scatter(
                [x_pos],
                [y],
                zorder=z_index,
                **_build_scatter_marker_params(style),
            )


def _resolve_marker_base_style(
    options: MarkerOptions | None,
    override: MarkerOptions | None,
) -> MarkerStyle:
    values: dict[str, object | None] = {}
    if options is not None:
        values.update(
            options.model_dump(
                exclude_none=True,
                exclude=["rules"],
                by_alias=False,
            )
        )
    if override is not None:
        values.update(
            override.model_dump(
                exclude_none=True,
                exclude=["rules"],
                by_alias=False,
            )
        )

    return MarkerStyle(**values)


def _resolve_marker_style(
    base_style: MarkerStyle,
    rules: list[MarkerStyleRule],
    context: DataContext,
) -> MarkerStyle:
    values = base_style.model_dump(exclude_none=True, by_alias=False)

    for rule in rules:
        if match_data_condition(rule.when, context=context):
            values.update(
                rule.style.model_dump(
                    exclude_none=True,
                    by_alias=False,
                )
            )

    return MarkerStyle(**values)


def _build_scatter_marker_params(style: MarkerStyle) -> dict[str, object]:
    params: dict[str, object] = {}

    if style.marker is not None:
        params["marker"] = to_mpl_marker_shape(style.marker)

    if style.markersize is not None:
        # plot.markersize 是直径 points，scatter.s 是面积 points^2。
        params["s"] = style.markersize**2

    if style.marker_facecolor is not None:
        params["facecolors"] = style.marker_facecolor

    if style.marker_edgecolor is not None:
        params["edgecolors"] = style.marker_edgecolor

    if style.marker_edgewidth is not None:
        params["linewidths"] = style.marker_edgewidth

    return params
