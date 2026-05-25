from collections.abc import Generator
from contextlib import AbstractContextManager, contextmanager

import matplotlib as mpl

from athena_charts_matplotlib.rendering.rcparams import build_rc_params
from athena_charts_matplotlib.styles import MatplotlibStyle


class MatplotlibPipelineContext:
    def __init__(self, style: MatplotlibStyle | None = None):
        self._style = style

    def pipeline_context(self) -> AbstractContextManager[None]:
        return matplotlib_theme_context(self._style)


@contextmanager
def matplotlib_theme_context(style: MatplotlibStyle) -> Generator[None, None, None]:
    with mpl.rc_context(build_rc_params(style)):
        yield
