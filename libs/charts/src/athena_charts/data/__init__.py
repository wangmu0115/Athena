from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_charts.data.base import (
        BarPlotData,
        LinePlotData,
        PiePlotData,
    )
    from athena_charts.data.categorical import CategoricalDatum, CategoricalSeriesData
    from athena_charts.data.xy import XYPoint, XYSeriesData


__all__ = (
    "BarPlotData",
    "LinePlotData",
    "PiePlotData",
    "CategoricalDatum",
    "CategoricalSeriesData",
    "XYPoint",
    "XYSeriesData",
)


_dynamic_imports = {
    "BarPlotData": "base",
    "LinePlotData": "base",
    "PiePlotData": "base",
    "CategoricalDatum": "categorical",
    "CategoricalSeriesData": "categorical",
    "XYPoint": "xy",
    "XYSeriesData": "xy",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
