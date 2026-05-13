from typing import TYPE_CHECKING

from athena_core.import_utils import import_attr

if TYPE_CHECKING:
    from athena_charts.themes.base import FigureTheme
    from athena_charts.themes.default import DEFAULT_FIGURE_THEME

__all__ = (
    "FigureTheme",
    "DEFAULT_FIGURE_THEME",
)

_dynamic_imports = {
    "FigureTheme": "base",
    "DEFAULT_FIGURE_THEME": "default",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
