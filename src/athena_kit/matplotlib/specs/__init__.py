from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.matplotlib.specs.chart import ChartSpec
    from athena_kit.matplotlib.specs.figure import ChartPlacement, FigureGridLayout, FigureSpec


__all__ = (
    "ChartPlacement",
    "FigureGridLayout",
    "FigureSpec",
    "ChartSpec",
)


_dynamic_imports = {
    "ChartPlacement": "figure",
    "FigureGridLayout": "figure",
    "FigureSpec": "figure",
    "ChartSpec": "chart",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
