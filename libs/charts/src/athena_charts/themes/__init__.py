from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_charts.themes.base import (
        AxisTheme,
        ChartTheme,
        FigureTheme,
        GridTheme,
        LegendTheme,
        PaletteTheme,
        PlotTheme,
        TextTheme,
        Theme,
    )
    from athena_charts.themes.default import DEFAULT_THEME


__all__ = (
    "DEFAULT_THEME",
    "TextTheme",
    "Theme",
    "PaletteTheme",
    "FigureTheme",
    "ChartTheme",
    "GridTheme",
    "LegendTheme",
    "AxisTheme",
    "PlotTheme",
)


_dynamic_imports = {
    "DEFAULT_THEME": "default",
    "TextTheme": "base",
    "Theme": "base",
    "PaletteTheme": "base",
    "FigureTheme": "base",
    "ChartTheme": "base",
    "GridTheme": "base",
    "LegendTheme": "base",
    "AxisTheme": "base",
    "PlotTheme": "base",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
