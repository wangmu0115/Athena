from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_matplotlib.options.axis import AxisLabelOptions, AxisOptions, AxisSpineOptions
    from athena_matplotlib.options.cartesian import CartesianCoordOptions
    from athena_matplotlib.options.chart import ChartOptions
    from athena_matplotlib.options.grid import GridOptions
    from athena_matplotlib.options.line_plot import (
        DataLabelOptions,
        LineOptions,
        LinePlotOptions,
        MarkerOptions,
    )
    from athena_matplotlib.options.renderfig import RenderFigureOptions
    from athena_matplotlib.options.savefig import PngExportStyle, SaveFigureOptions
    from athena_matplotlib.options.tick import TickLabelOptions, TickLineOptions, TickOptions


__all__ = (
    "AxisLabelOptions",
    "AxisOptions",
    "AxisSpineOptions",
    "PngExportStyle",
    "SaveFigureOptions",
    "RenderFigureOptions",
    "ChartOptions",
    "CartesianCoordOptions",
    "GridOptions",
    "TickLabelOptions",
    "TickLineOptions",
    "TickOptions",
    "DataLabelOptions",
    "LineOptions",
    "LinePlotOptions",
    "MarkerOptions",
)


_dynamic_imports = {
    "AxisLabelOptions": "axis",
    "AxisOptions": "axis",
    "AxisSpineOptions": "axis",
    "PngExportStyle": "savefig",
    "SaveFigureOptions": "savefig",
    "RenderFigureOptions": "renderfig",
    "ChartOptions": "chart",
    "CartesianCoordOptions": "cartesian",
    "GridOptions": "grid",
    "TickLabelOptions": "tick",
    "TickLineOptions": "tick",
    "TickOptions": "tick",
    "DataLabelOptions": "line_plot",
    "LineOptions": "line_plot",
    "LinePlotOptions": "line_plot",
    "MarkerOptions": "line_plot",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
