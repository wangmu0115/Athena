from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.matplotlib.styles.base import FontStyle, PaletteStyle
    from athena_kit.matplotlib.styles.chart import ChartStyle
    from athena_kit.matplotlib.styles.coord import AxisStyle
    from athena_kit.matplotlib.styles.figure import FigureStyle
    from athena_kit.matplotlib.styles.grid import GridStyle
    from athena_kit.matplotlib.styles.legend import LegendStyle
    from athena_kit.matplotlib.styles.plot import LinePlotStyle
    from athena_kit.matplotlib.styles.theme import Theme
    from athena_kit.matplotlib.styles.tick import TickLabelStyle, TickLineStyle, TickStyle


__all__ = (
    "FontStyle",
    "PaletteStyle",
    "FigureStyle",
    "ChartStyle",
    "AxisStyle",
    "GridStyle",
    "TickLabelStyle",
    "TickLineStyle",
    "TickStyle",
    "LegendStyle",
    "LinePlotStyle",
    "Theme",
)


_dynamic_imports = {
    "FontStyle": "base",
    "PaletteStyle": "base",
    "FigureStyle": "figure",
    "ChartStyle": "chart",
    "AxisStyle": "coord",
    "GridStyle": "grid",
    "TickLabelStyle": "tick",
    "TickLineStyle": "tick",
    "TickStyle": "tick",
    "LegendStyle": "legend",
    "LinePlotStyle": "plot",
    "Theme": "theme",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
