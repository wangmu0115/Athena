from collections.abc import Generator
from contextlib import contextmanager

import matplotlib as mpl

from athena_charts.themes import Theme
from athena_charts.themes.base import FigureTheme, TextTheme
from athena_charts_matplotlib.options.base import MatplotlibFigureOptions, MatplotlibOptions
from athena_core.functional.coalesce import first_not_none
from athena_core.functional.optionals import map_optional


@contextmanager
def matplotlib_theme_context(theme: Theme, options: MatplotlibOptions) -> Generator[None, None, None]:
    with mpl.rc_context(build_rc_params(theme, options)):
        yield


def build_rc_params(theme: Theme, options: MatplotlibOptions):
    """
    See `matplotlibrc` file or `matplotlib.rcParams` for a full list of configurable rcParams:
        - https://matplotlib.org/stable/users/explain/customizing.html#customizing-with-matplotlibrc-files
        - https://matplotlib.org/stable/api/matplotlib_configuration_api.html#matplotlib.rcParams
    """

    rc_params: dict[str, object] = {}
    if theme.text is not None:
        _update_from_text(theme.text, rc_params=rc_params)

    # figure.xxx
    rc_params.update(_build_figure_rc_params(theme.figure, options.figure))

    return rc_params


def _update_from_text(text: TextTheme, *, rc_params: dict[str, object]):
    if text.color:
        rc_params["text.color"] = text.color
    if text.font_family:
        rc_params["font.family"] = text.font_family
    if text.sans_serif_fonts:
        rc_params["font.sans-serif"] = text.sans_serif_fonts


def _build_figure_rc_params(theme: FigureTheme, options: MatplotlibFigureOptions):
    _rc_params: dict[str, object] = {}
    # figure.dpi
    dpi = map_optional(options, lambda x: x.dpi)
    if dpi is not None:
        _rc_params["figure.dpi"] = dpi
    # figure.figsize
    width = first_not_none(map_optional(options, lambda x: x.width), map_optional(theme, lambda x: x.width))
    height = first_not_none(map_optional(options, lambda x: x.height), map_optional(theme, lambda x: x.height))
    if width is not None and height is not None:
        nonull_dpi = dpi if dpi is not None else mpl.rcParamsDefault("figure.dpi")
        _rc_params["figure.figsize"] = (width / nonull_dpi, height / nonull_dpi)
    # figure.facecolor
    bg_color = first_not_none(map_optional(options, lambda x: x.background_color), map_optional(theme, lambda x: x.background_color))
    if bg_color:
        _rc_params["figure.facecolor"] = bg_color
    # figure.edgecolor
    edge_color = first_not_none(map_optional(options, lambda x: x.edge_color), map_optional(theme, lambda x: x.edge_color))
    if bg_color:
        _rc_params["figure.edgecolor"] = edge_color
    # figure.titlesize, figure.titleweight
    title_size = first_not_none(map_optional(options, lambda x: x.title_font_size), map_optional(theme, lambda x: x.title_font_size))
    if title_size:
        _rc_params["figure.titlesize"] = title_size
    title_weight = map_optional(options, lambda op: op.title_font_weight)
    if title_weight:
        _rc_params["figure.titleweight"] = title_weight
