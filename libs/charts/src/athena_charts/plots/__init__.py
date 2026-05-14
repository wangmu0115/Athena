from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_charts.plots.bar import BarPlot
    from athena_charts.plots.base import (
        Plot,
        PlotKind,
        PlotSpec,
    )
    from athena_charts.plots.data import (
        CategoricalDatum,
        PiePlotData,
        XYPlotData,
    )
    from athena_charts.plots.line import LinePlot
    from athena_charts.plots.options import (
        BarPlotOptions,
        CartesianPlotOptions,
        LinePlotOptions,
        PiePlotOptions,
        PlotOptions,
        PolarPlotOptions,
    )
    from athena_charts.plots.pie import PiePlot


__all__ = (
    "Plot",
    "PlotKind",
    "PlotSpec",
    "CategoricalDatum",
    "PiePlotData",
    "XYPlotData",
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
    "PlotSpec": "base",
    "CategoricalDatum": "data",
    "PiePlotData": "data",
    "XYPlotData": "data",
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
