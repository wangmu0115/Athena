from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_charts.specs.coords.axis import AxisOptions, AxisSpec
    from athena_charts.specs.coords.base import Coord
    from athena_charts.specs.coords.cartesian import (
        CartesianAxisSpec,
        CartesianCoord,
        CartesianGridOptions,
    )
    from athena_charts.specs.coords.polar import PolarAxisSpec, PolarCoord
    from athena_charts.specs.coords.ticks import (
        TickLabelFormat,
        TickLocator,
        TickOptions,
    )
    from athena_charts.specs.coords.types import (
        AxisDataType,
        AxisScale,
        CartesianAxisPosition,
        CoordKind,
        PolarAxisRole,
        TickLabelFormatKind,
        TickLocatorStrategy,
    )
    from athena_charts.specs.coords.unions import CoordSpec


__all__ = (
    "CoordSpec",
    "AxisOptions",
    "AxisSpec",
    "Coord",
    "CartesianAxisSpec",
    "CartesianCoord",
    "CartesianGridOptions",
    "PolarAxisSpec",
    "PolarCoord",
    "TickLabelFormat",
    "TickLocator",
    "TickOptions",
    "AxisDataType",
    "AxisScale",
    "CartesianAxisPosition",
    "CoordKind",
    "PolarAxisRole",
    "TickLabelFormatKind",
    "TickLocatorStrategy",
)


_dynamic_imports = {
    "CoordSpec": "unions",
    "AxisOptions": "axis",
    "AxisSpec": "axis",
    "Coord": "base",
    "CartesianAxisSpec": "cartesian",
    "CartesianCoord": "cartesian",
    "CartesianGridOptions": "cartesian",
    "PolarAxisSpec": "polar",
    "PolarCoord": "polar",
    "TickLabelFormat": "ticks",
    "TickLocator": "ticks",
    "TickOptions": "ticks",
    "AxisDataType": "types",
    "AxisScale": "types",
    "CartesianAxisPosition": "types",
    "CoordKind": "types",
    "PolarAxisRole": "types",
    "TickLabelFormatKind": "types",
    "TickLocatorStrategy": "types",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
