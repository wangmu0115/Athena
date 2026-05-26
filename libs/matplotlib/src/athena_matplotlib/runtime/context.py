from collections.abc import Callable
from typing import Any

from cycler import cycler

import matplotlib as mpl
from athena_core.values.optional import optional_or_else, safe_getattr
from athena_matplotlib.adapters import (
    to_mpl_legend_loc,
    to_mpl_line_style,
    to_mpl_marker_shape,
)
from athena_matplotlib.styles import (
    AxisStyle,
    ChartStyle,
    FigureStyle,
    FontStyle,
    GridStyle,
    LegendStyle,
    LinePlotStyle,
    Theme,
    TickStyle,
)


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


def build_rc_params(theme: Theme):
    """
    See `matplotlibrc` file or `matplotlib.rcParams` for a full list of configurable rcParams:
        - https://matplotlib.org/stable/users/explain/customizing.html#customizing-with-matplotlibrc-files
        - https://matplotlib.org/stable/api/matplotlib_configuration_api.html#matplotlib.rcParams
    """
    builder = RcParamsBuilder()
    if theme.palette is not None and theme.palette.colors:  # 调色板
        builder.set("axes.prop_cycle", cycler(color=theme.palette.colors))

    _resolve_font_rc_params(builder, theme.font)
    _resolve_figure_rc_params(builder, theme.figure)
    _resolve_chart_rc_params(builder, theme.chart)
    _resolve_axis_rc_params(builder, theme.axis)
    _resolve_grid_rc_params(builder, theme.grid)
    _resolve_tick_rc_params(builder, theme.tick)
    _resolve_legend_rc_params(builder, theme.legend)
    _resolve_line_plot_rc_params(builder, theme.line_plot)

    return builder.rc_params


def _resolve_font_rc_params(builder: RcParamsBuilder, style: FontStyle):
    if style is None:
        return

    font_family = safe_getattr(style, "family")
    if font_family is not None:
        builder.set("font.family", font_family)
        builder.set_non_empty(f"font.{font_family}", style=style, attr="fallbacks")
    builder.set_not_none("font.size", style=style, attr="size")
    builder.set_non_empty("font.weight", style=style, attr="weight")
    builder.set_non_empty("text.color", style=style, attr="color")


def _resolve_figure_rc_params(builder: RcParamsBuilder, style: FigureStyle):
    if style is None:
        return

    dpi = optional_or_else(safe_getattr(style, "dpi"), default_factory=lambda: mpl.rcParamsDefault["figure.dpi"])
    builder.set("figure.dpi", dpi)
    width, height = safe_getattr(style, "size")
    if width is not None and height is not None:
        builder.set("figure.figsize", (width / dpi, height / dpi))
    builder.set_non_empty("figure.facecolor", style=style, attr="facecolor")
    builder.set_non_empty("figure.edgecolor", style=style, attr="edgecolor")
    builder.set_not_none("figure.titlesize", style=style, attr="titlesize")
    builder.set_non_empty("figure.titleweight", style=style, attr="titleweight")


def _resolve_chart_rc_params(builder: RcParamsBuilder, style: ChartStyle):
    if style is None:
        return

    builder.set_non_empty("axes.facecolor", style=style, attr="facecolor")
    builder.set_not_none("axes.titlesize", style=style, attr="titlesize")
    builder.set_non_empty("axes.titleweight", style=style, attr="titleweight")
    builder.set_non_empty("axes.titlecolor", style=style, attr="titlecolor")


def _resolve_axis_rc_params(builder: RcParamsBuilder, style: AxisStyle):
    if style is None:
        return

    builder.set_non_empty("axes.edgecolor", style=style, attr="linecolor")
    builder.set_not_none("axes.linewidth", style=style, attr="linewidth")
    builder.set_not_none("axes.labelsize", style=style, attr="labelsize")
    builder.set_non_empty("axes.labelweight", style=style, attr="labelweight")
    builder.set_non_empty("axes.labelcolor", style=style, attr="labelcolor")


def _resolve_grid_rc_params(builder: RcParamsBuilder, style: GridStyle):
    if style is None:
        return

    builder.set_not_none("axes.grid", style=style, attr="visible")
    builder.set_non_empty("axes.grid.axis", style=style, attr="grid_axis")
    builder.set_non_empty("grid.color", style=style, attr="linecolor")
    builder.set_not_none("grid.linewidth", style=style, attr="linewidth")
    builder.set_non_empty("grid.linestyle", style=style, attr="linestyle", mapper=to_mpl_line_style)
    builder.set_not_none("grid.alpha", style=style, attr="alpha")


def _resolve_tick_rc_params(builder: RcParamsBuilder, style: TickStyle):
    if style is None:
        return

    # tick visible
    if style.line_visible:
        top, bottom, left, right = style.line_visible
        builder.set("xtick.top", top)
        builder.set("xtick.bottom", bottom)
        builder.set("ytick.left", left)
        builder.set("ytick.right", right)
    if style.label_visible:
        labeltop, labelbottom, labelleft, labelright = style.label_visible
        builder.set("xtick.labeltop", labeltop)
        builder.set("xtick.labelbottom", labelbottom)
        builder.set("ytick.labelleft", labelleft)
        builder.set("ytick.labelright", labelright)
    # tick line style
    builder.set_non_empty("xtick.color", style=style.line, attr="linecolor")
    builder.set_not_none("xtick.major.width", style=style.line, attr="linewidth")
    builder.set_not_none("xtick.major.size", style=style.line, attr="linelength")
    builder.set_non_empty("xtick.direction", style=style.line, attr="direction")
    builder.set_non_empty("ytick.color", style=style.line, attr="linecolor")
    builder.set_not_none("ytick.major.width", style=style.line, attr="linewidth")
    builder.set_not_none("ytick.major.size", style=style.line, attr="linelength")
    builder.set_non_empty("ytick.direction", style=style.line, attr="direction")
    # tick label
    builder.set_non_empty("xtick.labelcolor", style=style.label, attr="labelcolor")
    builder.set_not_none("xtick.labelsize", style=style.label, attr="labelsize")
    builder.set_non_empty("ytick.labelcolor", style=style.label, attr="labelcolor")
    builder.set_not_none("ytick.labelsize", style=style.label, attr="labelsize")


def _resolve_legend_rc_params(builder: RcParamsBuilder, style: LegendStyle):
    if style is None:
        return

    builder.set_non_empty("legend.loc", style=style, attr="location", mapper=to_mpl_legend_loc)
    builder.set_not_none("legend.title_fontsize", style=style, attr="titlesize")
    builder.set_not_none("legend.fontsize", style=style, attr="labelsize")
    builder.set_non_empty("legend.labelcolor", style=style, attr="labelcolor")
    builder.set_not_none("legend.frameon", style=style, attr="frameon")
    builder.set_not_none("legend.framealpha", style=style, attr="framealpha")
    builder.set_non_empty("legend.facecolor", style=style, attr="facecolor")
    builder.set_non_empty("legend.edgecolor", style=style, attr="edgecolor")
    builder.set_not_none("legend.shadow", style=style, attr="shadow")
    builder.set_not_none("legend.fancybox", style=style, attr="fancybox")


def _resolve_line_plot_rc_params(builder: RcParamsBuilder, style: LinePlotStyle):
    if style is None:
        return

    builder.set_not_none("lines.linewidth", style=style, attr="linewidth")
    builder.set_non_empty("lines.linestyle", style=style, attr="linestyle", mapper=to_mpl_line_style)
    builder.set_non_empty("lines.marker", style=style, attr="marker", mapper=to_mpl_marker_shape)
    builder.set_not_none("lines.markersize", style=style, attr="marker_size")
    builder.set_not_none("lines.markeredgewidth", style=style, attr="marker_edgewidth")
