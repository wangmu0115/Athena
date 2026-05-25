from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_matplotlib.styles.base import FontStyle, PaletteStyle
    from athena_matplotlib.styles.figure import FigureStyle
    # from athena_charts_matplotlib.styles.chart import AxisLineVisible, ChartStyle
    # from athena_charts_matplotlib.styles.coord import (
    #     AxisStyle,
    #     GridStyle,
    #     TickLabelStyle,
    #     TickLineStyle,
    #     TickStyle,
    #     TickVisible,
    # )
    # from athena_charts_matplotlib.styles.figure import FigureStyle
    # from athena_charts_matplotlib.styles.legend import LegendStyle
    # from athena_charts_matplotlib.styles.plot import LinePlotStyle
    # from athena_charts_matplotlib.styles.types import (
    #     FontFamily,
    #     FontWeight,
    #     GridAxis,
    #     LegendLocation,
    #     LineStyle,
    #     MarkerShape,
    #     TickDirection,
    # )
    # from athena_charts_matplotlib.styles.unions import MatplotlibStyle


__all__ = (
    "FontStyle",
    "PaletteStyle",
    "FigureStyle",
    # "AxisLineVisible",
    # "ChartStyle",
    # "AxisStyle",
    # "GridStyle",
    # "TickLabelStyle",
    # "TickLineStyle",
    # "TickVisible",
    # "TickStyle",
    # "LegendStyle",
    # "LinePlotStyle",
    # "MatplotlibStyle",
    # "FontFamily",
    # "FontWeight",
    # "GridAxis",
    # "LegendLocation",
    # "LineStyle",
    # "MarkerShape",
    # "TickDirection",
)


_dynamic_imports = {
    "FontStyle": "base",
    "PaletteStyle": "base",
    "FigureStyle": "figure",
    # "AxisLineVisible": "chart",
    # "ChartStyle": "chart",
    # "AxisStyle": "coord",
    # "GridStyle": "coord",
    # "TickLabelStyle": "coord",
    # "TickLineStyle": "coord",
    # "TickVisible": "coord",
    # "TickStyle": "coord",
    # "LegendStyle": "legend",
    # "LinePlotStyle": "plot",
    # "MatplotlibStyle": "unions",
    # "FontFamily": "types",
    # "FontWeight": "types",
    # "GridAxis": "types",
    # "LegendLocation": "types",
    # "LineStyle": "types",
    # "MarkerShape": "types",
    # "TickDirection": "types",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
