from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_charts.specs.figures.figure import ChartPlacement, FigureSpec
    from athena_charts.specs.figures.labels import FigureLabels
    from athena_charts.specs.figures.layout import FigureGridLayout
    from athena_charts.specs.figures.options import FigureOptions


__all__ = (
    "ChartPlacement",
    "FigureSpec",
    "FigureLabels",
    "FigureGridLayout",
    "FigureOptions",
)

_dynamic_imports = {
    "ChartPlacement": "figure",
    "FigureSpec": "figure",
    "FigureLabels": "labels",
    "FigureGridLayout": "layout",
    "FigureOptions": "options",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
