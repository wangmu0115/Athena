"""Theme 描述跨引擎视觉语义"""

from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_charts.themes.chart import ChartTheme
    from athena_charts.themes.coord import AxisTheme, GridTheme, TickTheme
    from athena_charts.themes.figure import FigureTheme
    from athena_charts.themes.font import FontTheme
    from athena_charts.themes.legend import LegendTheme
    from athena_charts.themes.palette import PaletteTheme
    from athena_charts.themes.plot import PlotTheme
    from athena_charts.themes.types import (
        FontWeight,
        LegendDirection,
        LegendLocation,
        LineStyle,
        TickDirection,
    )
    from athena_charts.themes.unions import Theme


__all__ = (
    "ChartTheme",
    "AxisTheme",
    "GridTheme",
    "TickTheme",
    "FigureTheme",
    "FontTheme",
    "LegendTheme",
    "PaletteTheme",
    "PlotTheme",
    "FontWeight",
    "LegendDirection",
    "LegendLocation",
    "LineStyle",
    "TickDirection",
    "Theme",
)


_dynamic_imports = {
    "ChartTheme": "chart",
    "AxisTheme": "coord",
    "GridTheme": "coord",
    "TickTheme": "coord",
    "FigureTheme": "figure",
    "FontTheme": "font",
    "LegendTheme": "legend",
    "PaletteTheme": "palette",
    "PlotTheme": "plot",
    "FontWeight": "types",
    "LegendDirection": "types",
    "LegendLocation": "types",
    "LineStyle": "types",
    "TickDirection": "types",
    "Theme": "unions",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
