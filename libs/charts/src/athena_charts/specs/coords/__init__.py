from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_charts.options.coord import CartesianGridOptions
    from athena_charts.specs.coords.axis import (
        AxisSpec,
        CartesianAxis,
        PolarAxis,
        TickFormatter,
        TickOptions,
    )
    from athena_charts.specs.coords.cartesian import CartesianCoord
    from athena_charts.specs.coords.base import Coord
    from athena_charts.specs.coords.polar import PolarCoord
    from athena_charts.specs.coords.types import (
        AxisDataType,
        CoordKind,
        TickFormatterKind,
    )
    from athena_charts.specs.coords.unions import CoordSpec


__all__ = (
    "AxisSpec",
    "CartesianAxis",
    "PolarAxis",
    "TickFormatter",
    "TickOptions",
    "Coord",
    "CoordSpec",
    "CartesianCoord",
    "CartesianGridOptions",
    "PolarCoord",
    "AxisDataType",
    "CoordKind",
    "TickFormatterKind",
)


_dynamic_imports = {
    "AxisSpec": "axis",
    "CartesianAxis": "axis",
    "PolarAxis": "axis",
    "TickFormatter": "axis",
    "TickOptions": "axis",
    "Coord": "base",
    "CoordSpec": "union",
    "CartesianCoord": "cartesian",
    "CartesianGridOptions": "options",
    "PolarCoord": "polar",
    "AxisDataType": "types",
    "CoordKind": "types",
    "TickFormatterKind": "types",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
