from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_matplotlib.options.plots.bar import (
        BarLayoutOptions,
        BarOptions,
        BarPlotOptions,
    )
    from athena_matplotlib.options.plots.data_label import (
        DataLabelOptions,
        DataLabelStyle,
        DataLabelStyleRule,
    )
    from athena_matplotlib.options.plots.line import LineOptions, LinePlotOptions
    from athena_matplotlib.options.plots.marker import (
        MarkerOptions,
        MarkerStyle,
        MarkerStyleRule,
    )


__all__ = (
    "BarLayoutOptions",
    "BarOptions",
    "BarPlotOptions",
    "LineOptions",
    "LinePlotOptions",
    "DataLabelOptions",
    "DataLabelStyle",
    "DataLabelStyleRule",
    "MarkerOptions",
    "MarkerStyle",
    "MarkerStyleRule",
)


_dynamic_imports = {
    "BarLayoutOptions": "bar",
    "BarOptions": "bar",
    "BarPlotOptions": "bar",
    "LineOptions": "line",
    "LinePlotOptions": "line",
    "DataLabelOptions": "data_label",
    "DataLabelStyle": "data_label",
    "DataLabelStyleRule": "data_label",
    "MarkerOptions": "marker",
    "MarkerStyle": "marker",
    "MarkerStyleRule": "marker",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
