from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_charts.themes.base import DEFAULT_THEME, PaletteTheme, TextTheme, Theme
    from athena_charts.themes.chart import ChartTheme, GridTheme, LegendTheme
    from athena_charts.themes.coord import AxisTheme
    from athena_charts.themes.figure import FigureTheme
    from athena_charts.themes.plot import PlotTheme


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
    "DEFAULT_THEME": "base",
    "TextTheme": "base",
    "Theme": "base",
    "PaletteTheme": "base",
    "FigureTheme": "figure",
    "ChartTheme": "chart",
    "GridTheme": "chart",
    "LegendTheme": "chart",
    "AxisTheme": "coord",
    "PlotTheme": "plot",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
