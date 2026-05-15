from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_charts.specs.plots.bar import BarPlot
    from athena_charts.specs.plots.base import Plot, PlotKind
    from athena_charts.specs.plots.data import (
        BarPlotData,
        CategoricalDatum,
        CategoricalSeriesData,
        LinePlotData,
        PiePlotData,
        XYPoint,
        XYSeriesData,
    )
    from athena_charts.specs.plots.line import LinePlot
    from athena_charts.specs.plots.options import (
        BarPlotOptions,
        CartesianPlotOptions,
        LinePlotOptions,
        PiePlotOptions,
        PlotOptions,
        PolarPlotOptions,
    )
    from athena_charts.specs.plots.pie import PiePlot
    from athena_charts.specs.plots.union import PlotSpec


__all__ = (
    "Plot",
    "PlotKind",
    "PlotSpec",
    "BarPlotData",
    "CategoricalDatum",
    "CategoricalSeriesData",
    "LinePlotData",
    "PiePlotData",
    "XYPoint",
    "XYSeriesData",
    "BarPlotOptions",
    "CartesianPlotOptions",
    "LinePlotOptions",
    "PiePlotOptions",
    "PlotOptions",
    "PolarPlotOptions",
    "LinePlot",
    "BarPlot",
    "PiePlot",
)


_dynamic_imports = {
    "Plot": "base",
    "PlotKind": "base",
    "PlotSpec": "union",
    "BarPlotData": "data",
    "CategoricalDatum": "data",
    "CategoricalSeriesData": "data",
    "LinePlotData": "data",
    "PiePlotData": "data",
    "XYPoint": "data",
    "XYSeriesData": "data",
    "BarPlotOptions": "options",
    "CartesianPlotOptions": "options",
    "LinePlotOptions": "options",
    "PiePlotOptions": "options",
    "PlotOptions": "options",
    "PolarPlotOptions": "options",
    "LinePlot": "line",
    "BarPlot": "bar",
    "PiePlot": "pie",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
