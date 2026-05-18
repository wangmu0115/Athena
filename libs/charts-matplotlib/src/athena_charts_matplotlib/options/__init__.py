

from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_charts_matplotlib.options.base import (
        MatplotlibFigureOptions,
        MatplotlibFontOptions,
        MatplotlibOptions,
    )
    from athena_charts_matplotlib.options.preset.default import DEFAULT_MATPLOTLIB_OPTIONS


__all__ = (
    "DEFAULT_MATPLOTLIB_OPTIONS",
    "MatplotlibFigureOptions",
    "MatplotlibFontOptions",
    "MatplotlibOptions",
)


_dynamic_imports = {
    "DEFAULT_MATPLOTLIB_OPTIONS": "default",
    "MatplotlibFigureOptions": "base",
    "MatplotlibFontOptions": "base",
    "MatplotlibOptions": "base",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
