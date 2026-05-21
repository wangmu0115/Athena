from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_charts.specs.plots.bar import BarPlot
    from athena_charts.specs.plots.base import Plot
    from athena_charts.specs.plots.line import LinePlot
    from athena_charts.specs.plots.pie import PiePlot
    from athena_charts.specs.plots.types import (
        LineStyle,
        MarkerShape,
        PlotKind,
    )
    from athena_charts.specs.plots.unions import PlotSpec


__all__ = (
    "Plot",
    "PlotSpec",
    "LinePlot",
    "BarPlot",
    "PiePlot",
    "LineStyle",
    "MarkerShape",
    "PlotKind",
)


_dynamic_imports = {
    "Plot": "base",
    "PlotSpec": "union",
    "LinePlot": "line",
    "BarPlot": "bar",
    "PiePlot": "pie",
    "LineStyle": "types",
    "MarkerShape": "types",
    "PlotKind": "types",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
