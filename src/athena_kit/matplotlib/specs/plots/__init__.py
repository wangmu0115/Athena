from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.matplotlib.specs.plots.bar import BarPlot, BarPlotData
    from athena_kit.matplotlib.specs.plots.base import Plot
    from athena_kit.matplotlib.specs.plots.line import LinePlot
    from athena_kit.matplotlib.specs.plots.pie import PiePlot
    from athena_kit.matplotlib.specs.plots.unions import PlotSpec


__all__ = (
    "Plot",
    "PlotSpec",
    "LinePlot",
    "BarPlot",
    "PiePlot",
    "BarPlotData",
)


_dynamic_imports = {
    "Plot": "base",
    "PlotSpec": "unions",
    "LinePlot": "line",
    "BarPlot": "bar",
    "BarPlotData": "bar",
    "PiePlot": "pie",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
