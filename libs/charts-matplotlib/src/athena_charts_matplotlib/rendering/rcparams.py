from collections.abc import Callable
from typing import Any

import matplotlib as mpl

from athena_charts_matplotlib.adapters import (
    to_mpl_legend_loc,
    to_mpl_line_style,
    to_mpl_marker_shape,
)
from athena_charts_matplotlib.styles import MatplotlibStyle
from athena_core.values.optional import optional_or_else, safe_getattr


class RcParamsBuilder:
    def __init__(self):
        self._rc_params: dict[str, object] = {}

    @property
    def rc_params(self) -> dict[str, object]:
        """Return collected `rcParams`."""
        return self._rc_params

    def set(self, key: str, value: object | None):
        if value is not None:
            self._rc_params[key] = value

    def set_not_none(
        self,
        key: str,
        *,
        style: object | None,
        attr: str,
        mapper: Callable[[Any], object | None] | None = None,
    ) -> None:
        value = safe_getattr(style, attr)
        if value is None:
            return
        if mapper is not None:
            value = mapper(value)
        self.set(key, value)

    def set_non_empty(
        self,
        key: str,
        *,
        style: object | None,
        attr: str,
        mapper: Callable[[Any], object | None] | None = None,
    ):
        value = safe_getattr(style, attr)
        if value is None or len(value) == 0:
            return
        if mapper is not None:
            value = mapper(value)
        self.set(key, value)


def build_rc_params(style: MatplotlibStyle):
    """
    See `matplotlibrc` file or `matplotlib.rcParams` for a full list of configurable rcParams:
        - https://matplotlib.org/stable/users/explain/customizing.html#customizing-with-matplotlibrc-files
        - https://matplotlib.org/stable/api/matplotlib_configuration_api.html#matplotlib.rcParams
    """
    builder = RcParamsBuilder()
    builder.set_non_empty("axes.prop_cycle", style=style.palette, attr="colors")

    _resolve_font_rc_params(builder, style)
    _resolve_figure_rc_params(builder, style)
    _resolve_chart_rc_params(builder, style)
    _resolve_coord_axis_rc_params(builder, style)
    _resolve_coord_grid_rc_params(builder, style)
    _resolve_coord_tick_rc_params(builder, style)
    _resolve_legend_rc_params(builder, style)
    _resolve_line_plot_rc_params(builder, style)

    return builder.rc_params


def _resolve_font_rc_params(builder: RcParamsBuilder, style: MatplotlibStyle):
    font_family = safe_getattr(style.font, "family")
    if font_family is not None:
        builder.set("font.family", font_family)
        builder.set_non_empty(f"font.{font_family}", style=style.font, attr="fallbacks")
    builder.set_not_none("font.size", style=style.font, attr="size")
    builder.set_non_empty("font.weight", style=style.font, attr="weight")
    builder.set_non_empty("text.color", style=style.font, attr="color")


def _resolve_figure_rc_params(builder: RcParamsBuilder, style: MatplotlibStyle):
    dpi = optional_or_else(safe_getattr(style.figure, "dpi"), default_factory=lambda: mpl.rcParamsDefault["figure.dpi"])
    builder.set("figure.dpi", dpi)
    width, height = safe_getattr(style.figure, "size")
    if width is not None and height is not None:
        builder.set("figure.figsize", (width / dpi, height / dpi))

    builder.set_non_empty("figure.facecolor", style=style.figure, attr="facecolor")
    builder.set_non_empty("figure.edgecolor", style=style.figure, attr="edgecolor")
    builder.set_not_none("figure.titlesize", style=style.figure, attr="titlesize")
    builder.set_non_empty("figure.titleweight", style=style.figure, attr="titleweight")


def _resolve_chart_rc_params(builder: RcParamsBuilder, style: MatplotlibStyle):
    if style.chart is None:
        return
    builder.set_non_empty("axes.facecolor", style=style.chart, attr="facecolor")
    builder.set_not_none("axes.titlesize", style=style.chart, attr="titlesize")
    builder.set_non_empty("axes.titleweight", style=style.chart, attr="titleweight")
    builder.set_non_empty("axes.titlecolor", style=style.chart, attr="titlecolor")
    if style.chart.axis_line_visible is not None:
        builder.set_not_none("axes.spines.top", style=style.chart.axis_line_visible, attr="top")
        builder.set_not_none("axes.spines.bottom", style=style.chart.axis_line_visible, attr="bottom")
        builder.set_not_none("axes.spines.left", style=style.chart.axis_line_visible, attr="left")
        builder.set_not_none("axes.spines.right", style=style.chart.axis_line_visible, attr="right")


def _resolve_coord_axis_rc_params(builder: RcParamsBuilder, style: MatplotlibStyle):
    if style.axis is None:
        return
    builder.set_non_empty("axes.edgecolor", style=style.axis, attr="linecolor")
    builder.set_not_none("axes.linewidth", style=style.axis, attr="linewidth")
    builder.set_not_none("axes.labelsize", style=style.axis, attr="labelsize")
    builder.set_non_empty("axes.labelweight", style=style.axis, attr="labelweight")
    builder.set_non_empty("axes.labelcolor", style=style.axis, attr="labelcolor")


def _resolve_coord_grid_rc_params(builder: RcParamsBuilder, style: MatplotlibStyle):
    if style.grid is None:
        return
    builder.set_not_none("axes.grid", style=style.grid, attr="visible")
    builder.set_non_empty("axes.grid.axis", style=style.grid, attr="grid_axis")
    builder.set_non_empty("grid.color", style=style.grid, attr="linecolor")
    builder.set_not_none("grid.linewidth", style=style.grid, attr="linewidth")
    builder.set_non_empty("grid.linestyle", style=style.grid, attr="linestyle", mapper=to_mpl_line_style)
    builder.set_not_none("grid.alpha", style=style.grid, attr="alpha")


def _resolve_coord_tick_rc_params(builder: RcParamsBuilder, style: MatplotlibStyle):
    if style.tick is None:
        return
    # visible
    builder.set_not_none("xtick.top", style=style.tick.top, attr="line")
    builder.set_not_none("xtick.labeltop", style=style.tick.top, attr="label")
    builder.set_not_none("xtick.bottom", style=style.tick.bottom, attr="line")
    builder.set_not_none("xtick.labelbottom", style=style.tick.bottom, attr="label")
    builder.set_not_none("ytick.left", style=style.tick.left, attr="line")
    builder.set_not_none("ytick.labelleft", style=style.tick.left, attr="label")
    builder.set_not_none("ytick.right", style=style.tick.right, attr="line")
    builder.set_not_none("ytick.labelright", style=style.tick.right, attr="label")
    # tick line
    builder.set_not_none("xtick.color", style=style.tick.line, attr="linecolor")
    builder.set_not_none("xtick.major.width", style=style.tick.line, attr="linewidth")
    builder.set_not_none("xtick.major.size", style=style.tick.line, attr="linelength")
    builder.set_not_none("xtick.direction", style=style.tick.line, attr="direction")
    builder.set_not_none("ytick.color", style=style.tick.line, attr="linecolor")
    builder.set_not_none("ytick.major.width", style=style.tick.line, attr="linewidth")
    builder.set_not_none("ytick.major.size", style=style.tick.line, attr="linelength")
    builder.set_not_none("ytick.direction", style=style.tick.line, attr="direction")
    # tick label
    builder.set_not_none("xtick.labelcolor", style=style.tick.label, attr="labelsize")
    builder.set_not_none("xtick.labelsize", style=style.tick.label, attr="labelcolor")
    builder.set_not_none("ytick.labelcolor", style=style.tick.label, attr="labelsize")
    builder.set_not_none("ytick.labelsize", style=style.tick.label, attr="labelcolor")


def _resolve_legend_rc_params(builder: RcParamsBuilder, style: MatplotlibStyle):
    if style.legend is None:
        return
    builder.set_non_empty("legend.loc", style=style.legend, attr="location", mapper=to_mpl_legend_loc)
    builder.set_not_none("legend.title_fontsizee", style=style.legend, attr="titlesize")
    builder.set_not_none("legend.fontsize", style=style.legend, attr="labelsize")
    builder.set_non_empty("legend.labelcolor", style=style.legend, attr="labelcolor")

    builder.set_not_none("legend.frameon", style=style.legend, attr="frameon")
    builder.set_not_none("legend.framealpha", style=style.legend, attr="framealpha")
    builder.set_non_empty("legend.facecolor", style=style.legend, attr="facecolor")
    builder.set_non_empty("legend.edgecolor", style=style.legend, attr="edgecolor")
    builder.set_not_none("legend.shadow", style=style.legend, attr="shadow")
    builder.set_not_none("legend.fancybox", style=style.legend, attr="fancybox")


def _resolve_line_plot_rc_params(builder: RcParamsBuilder, style: MatplotlibStyle):
    if style.line_plot is None:
        return
    builder.set_not_none("lines.linewidth", style=style.line_plot, attr="linewidth")
    builder.set_non_empty("lines.linestyle", style=style.line_plot, attr="linestyle", mapper=to_mpl_line_style)
    builder.set_non_empty("lines.marker", style=style.line_plot, attr="marker", mapper=to_mpl_marker_shape)
    builder.set_not_none("lines.markersize", style=style.line_plot, attr="marker_size")
    builder.set_not_none("lines.markeredgewidth", style=style.line_plot, attr="marker_edgewidth")
