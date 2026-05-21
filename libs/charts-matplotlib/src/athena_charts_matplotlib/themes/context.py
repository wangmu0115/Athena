from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass

import matplotlib as mpl

from athena_charts.themes import Theme
from athena_charts.themes._base import FigureTheme, FontTheme
from athena_charts_matplotlib.options import (
    MatplotlibFontOptions,
    MatplotlibOptions,
)
from athena_charts_matplotlib.options.figure import MatplotlibFigureOptions
from athena_core.values.fallbacks import first_non_empty, first_not_none
from athena_core.values.optional import optional_map, optional_or_else, safe_getattr


class ColorCycle:
    def __init__(self, colors: list[str]):
        self._colors = colors or []
        self._n_colors = len(colors) if colors else 0
        self._index = 0

    def next(self) -> str | None:
        color = self.pick(self._index)
        if color is not None:
            self._index += 1
        return color

    def pick(self, index: int = 0) -> str | None:
        if self._n_colors == 0:
            return None
        color = self._colors[index % self._n_colors]
        return color


@dataclass
class MatplotlibRenderContext:
    palette: ColorCycle

    def __init__(self, theme: Theme, options: MatplotlibOptions):
        self.palette = ColorCycle(
            first_non_empty(
                safe_getattr(options.palette, "sequence"),
                safe_getattr(theme.palette, "sequence"),
            )
        )


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
    # font.xxx, text.color
    rc_params.update(_build_font_rc_params(theme.font, options.font))
    # figure.xxx
    rc_params.update(_build_figure_rc_params(theme.figure, options.figure))

    return rc_params


def _build_font_rc_params(theme: FontTheme, options: MatplotlibFontOptions):
    _rc_params: dict[str, object] = {}
    # font.family, font.{font.family}(e.g. font.sans-serif)
    font_family = first_not_none(safe_getattr(options, "family"), safe_getattr(theme, "family"))
    if font_family is not None:
        if font_family not in ("sans-serif", "serif", "monospace", "cursive", "fantasy"):
            raise ValueError(f"Unsupported font family: {font_family}.")
        _rc_params["font.family"] = font_family
        fonts = first_non_empty(safe_getattr(options, "fonts"), safe_getattr(theme, "fallbacks"))
        if fonts is not None:
            _rc_params[f"font.{font_family}"] = fonts
    # text.color
    text_color = first_non_empty(safe_getattr(options, "color"), optional_map(theme, "color"))
    if text_color is not None:
        _rc_params["text.color"] = text_color
    # font.weight
    font_weight = first_non_empty(safe_getattr(options, "wight"), optional_map(theme, "wight"))
    if font_weight is not None:
        _rc_params["font.weight"] = font_weight


def _build_figure_rc_params(theme: FigureTheme, options: MatplotlibFigureOptions) -> dict[str, object]:
    _rc_params: dict[str, object] = {}
    # figure.dpi
    dpi = safe_getattr(options, "dpi")
    if dpi is not None:
        _rc_params["figure.dpi"] = dpi
    # figure.figsize
    width, height = safe_getattr(options, "width"), safe_getattr(options, "height")
    if width is not None and height is not None:
        notnull_dpi = optional_or_else(dpi, default_factory=lambda: mpl.rcParamsDefault["figure.dpi"])
        _rc_params["figure.figsize"] = (width / notnull_dpi, height / notnull_dpi)
    # figure.facecolor
    bg_color = first_non_empty(safe_getattr(options, "facecolor"), safe_getattr(theme, "background_color"))
    if bg_color is not None:
        _rc_params["figure.facecolor"] = bg_color
    # figure.edgecolor
    edge_color = first_non_empty(safe_getattr(options, "edgecolor"), safe_getattr(theme, "edge_color"))
    if edge_color is not None:
        _rc_params["figure.edgecolor"] = edge_color
    # figure.titlesize,
    title_size = first_not_none(safe_getattr(options, "titlesize"), safe_getattr(theme, "title_font_size"))
    if title_size is not None:
        _rc_params["figure.titlesize"] = title_size
    # figure.titleweight
    title_weight = first_not_none(safe_getattr(options, "titleweight"), safe_getattr(theme, "title_font_weight"))
    if title_weight is not None:
        _rc_params["figure.titleweight"] = title_weight
