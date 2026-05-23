from collections.abc import Generator
from contextlib import contextmanager

import matplotlib as mpl

from athena_charts_matplotlib.rendering.rcparams import build_rc_params
from athena_charts_matplotlib.styles import MatplotlibStyle


@contextmanager
def matplotlib_theme_context(style: MatplotlibStyle) -> Generator[None, None, None]:
    with mpl.rc_context(build_rc_params(style)):
        yield
