from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass

import matplotlib as mpl

from athena_charts.themes import Theme
from athena_charts_matplotlib.rendering.colors import ColorCycle, build_color_cycle
from athena_charts_matplotlib.rendering.rcparams import build_rc_params
from athena_charts_matplotlib.styles import MatplotlibStyle


@dataclass
class MatplotlibRenderContext:
    colors: ColorCycle

    def __init__(self, theme: Theme, style: MatplotlibStyle):
        self.colors = build_color_cycle(theme.palette, style.palette)


@contextmanager
def matplotlib_theme_context(theme: Theme, style: MatplotlibStyle) -> Generator[None, None, None]:
    with mpl.rc_context(build_rc_params(theme, style)):
        yield
