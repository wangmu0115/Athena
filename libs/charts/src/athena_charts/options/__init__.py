from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_charts.options.chart import ChartOptions, LegendOptions
    from athena_charts.options.coord import CartesianGridOptions
    from athena_charts.options.plot import (
        BarPlotOptions,
        CartesianPlotOptions,
        LinePlotOptions,
        PiePlotOptions,
        PlotOptions,
    )


__all__ = (
    "ChartOptions",
    "LegendOptions",
    "CartesianGridOptions",
    "BarPlotOptions",
    "CartesianPlotOptions",
    "LinePlotOptions",
    "PiePlotOptions",
    "PlotOptions",
)


_dynamic_imports = {
    "ChartOptions": "chart",
    "LegendOptions": "chart",
    "CartesianGridOptions": "coord",
    "BarPlotOptions": "plot",
    "CartesianPlotOptions": "plot",
    "LinePlotOptions": "plot",
    "PiePlotOptions": "plot",
    "PlotOptions": "plot",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
