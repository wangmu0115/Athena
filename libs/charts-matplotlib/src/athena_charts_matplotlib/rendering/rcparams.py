from collections.abc import Callable
from typing import Any

import matplotlib as mpl

from athena_charts.themes import FigureTheme, FontTheme, GridTheme, Theme
from athena_charts_matplotlib.adapters import (
    to_mpl_font_weight,
    to_mpl_line_style,
)
from athena_charts_matplotlib.styles import (
    MatplotlibFigureStyle,
    MatplotlibFontStyle,
    MatplotlibStyle,
)
from athena_charts_matplotlib.styles.grid import MatplotlibGridStyle
from athena_core.values.fallbacks import first_non_empty, first_not_none
from athena_core.values.optional import optional_or_else, safe_getattr


class RcParamsBuilder:
    def __init__(self):
        self._rc_params: dict[str, object] = {}

    @property
    def rc_params(self) -> dict[str, object]:
        """Return collected `rcParams`."""
        return self._rc_params

    def set(self, param_key: str, value: object | None):
        if value is not None:
            self._rc_params[param_key] = value

    def get(self, param_key: str) -> object | None:
        return self._rc_params.get(param_key)

    def set_not_none(
        self,
        param_key: str,
        *obj_attrs: tuple[object | None, str],
        mapper: Callable[[Any], object | None] | None = None,
    ) -> None:
        value = first_not_none(*(safe_getattr(obj, attr) for obj, attr in obj_attrs))
        if value is None:
            return
        if mapper is not None:
            value = mapper(value)

        self.set(param_key, value)

    def set_non_empty(
        self,
        param_key: str,
        *obj_attrs: tuple[object | None, str],
        mapper: Callable[[Any], object | None] | None = None,
    ):
        value = first_non_empty(*(safe_getattr(obj, attr) for obj, attr in obj_attrs))
        if value is None:
            return
        if mapper is not None:
            value = mapper(value)

        self.set(param_key, value)


def build_rc_params(theme: Theme, style: MatplotlibStyle):
    """
    See `matplotlibrc` file or `matplotlib.rcParams` for a full list of configurable rcParams:
        - https://matplotlib.org/stable/users/explain/customizing.html#customizing-with-matplotlibrc-files
        - https://matplotlib.org/stable/api/matplotlib_configuration_api.html#matplotlib.rcParams
    """
    builder = RcParamsBuilder()

    resolve_font_rc_params(builder, theme.font, style.font)
    resolve_figure_rc_params(builder, theme.figure, style.figure)
    resolve_axes_rc_params(builder, theme, style)
    resolve_grid_rc_params(builder, theme.grid, style.grid)

    builder.set_non_empty("axes.prop_cycle", (style.palette, "sequence"), (theme.palette, "sequence"))

    return builder.rc_params


def resolve_font_rc_params(builder: RcParamsBuilder, theme: FontTheme, style: MatplotlibFontStyle):
    """解析 Font 相关的 `Matplotlib rcParams`。"""

    font_family = first_non_empty(safe_getattr(style, "family"), safe_getattr(theme, "family"))
    if _is_font_family(font_family):
        builder.set("font.family", font_family)
        builder.set_non_empty(
            f"font.{font_family}",
            (style, "fallbacks"),
            (theme, "fallbacks"),
        )
    builder.set_not_none("font.size", (style, "size"))
    builder.set_non_empty("font.weight", (style, "weight"), (theme, "weight"), mapper=to_mpl_font_weight)
    builder.set_non_empty("text.color", (style, "color"), (theme, "color"))


def resolve_figure_rc_params(builder: RcParamsBuilder, theme: FigureTheme, style: MatplotlibFigureStyle):
    """解析 Figure 相关的 `Matplotlib rcParams`。"""

    builder.set_not_none("figure.dpi", (style, "dpi"))
    width = safe_getattr(style, "width")
    height = safe_getattr(style, "height")
    if width is not None and height is not None:
        resolved_dpi = optional_or_else(builder.get("figure.dpi"), default_factory=lambda: mpl.rcParamsDefault["figure.dpi"])
        builder.set("figure.figsize", (width / resolved_dpi, height / resolved_dpi))
    builder.set_non_empty("figure.facecolor", (style, "facecolor"), (theme, "background_color"))
    builder.set_non_empty("figure.edgecolor", (style, "edgecolor"), (theme, "edge_color"))
    builder.set_not_none("figure.frameon", (style, "frameon"))
    builder.set_not_none("figure.titlesize", (style, "titlesize"), (style, "title_fontsize"))
    builder.set_not_none("figure.titleweight", (style, "titleweight"), (theme, "title_fontweight"))


def resolve_axes_rc_params(builder: RcParamsBuilder, theme: Theme, style: MatplotlibStyle):
    """解析 Axes 相关的 `Matplotlib rcParams`。"""

    builder.set_non_empty("axes.facecolor", (style.axes, "facecolor"), (theme.chart, "background_color"))
    builder.set_non_empty("axes.edgecolor", (style.axes, "edgecolor"), (theme.axis, "line_color"))
    builder.set_not_none("axes.linewidth", (style.axes, "edge_linewidth"), (theme.axis, "line_width"))

    builder.set_not_none("axes.titlesize", (style.axes, "titlesize"), (theme.chart, "title_fontsize"))
    builder.set_non_empty(
        "axes.titleweight",
        (style.axes, "titleweight"),
        (theme.chart, "title_fontweight"),
        mapper=to_mpl_font_weight,
    )
    builder.set_non_empty("axes.titlecolor", (style.axes, "titlecolor"), (theme.chart, "title_color"))
    builder.set_non_empty("axes.titlelocation", (style.axes, "titlelocation"))

    builder.set_not_none("axes.labelsize", (style.axes, "labelsize"), (theme.axis, "label_fontsize"))
    builder.set_non_empty(
        "axes.labelweight",
        (style.axes, "labelweight"),
        (theme.axis, "label_fontweight"),
        mapper=to_mpl_font_weight,
    )
    builder.set_non_empty("axes.labelcolor", (style.axes, "labelcolor"), (theme.axis, "label_color"))
    builder.set_non_empty("xaxis.labellocation", (style.axes, "x_axis_labellocation"))
    builder.set_non_empty("yaxis.labellocation", (style.axes, "y_axis_labellocation"))


def resolve_grid_rc_params(builder: RcParamsBuilder, theme: GridTheme, style: MatplotlibGridStyle):
    """解析 Grid 相关的 `Matplotlib rcParams`。"""
    builder.set_not_none("axes.grid", (style, "visible"))
    builder.set_non_empty("axes.grid.axis", (style, "grid_axis"))
    builder.set_non_empty("grid.color", (style, "line_color"), (theme, "line_color"))
    builder.set_not_none("grid.linewidth", (style, "line_width"), (theme, "line_width"))
    builder.set_non_empty(
        "grid.linestyle",
        (style, "line_style"),
        (theme, "line_style"),
        mapper=to_mpl_line_style,
    )
    builder.set_not_none("grid.alpha", (style, "alpha"), (theme, "alpha"))


def _is_font_family(value: str | None) -> bool:
    if value is None:
        return False
    return value in {"sans-serif", "serif", "monospace", "cursive", "fantasy"}
