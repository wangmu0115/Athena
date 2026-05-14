from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_charts.coords.axis import (
        BaseAxis,
        CartesianAxis,
        PolarAxis,
        TickFormatter,
        TickOptions,
    )
    from athena_charts.coords.base import Coord, CoordKind
    from athena_charts.coords.cartesian import CartesianCoord
    from athena_charts.coords.options import CartesianGridOptions
    from athena_charts.coords.polar import PolarCoord


__all__ = (
    "BaseAxis",
    "CartesianAxis",
    "PolarAxis",
    "TickFormatter",
    "TickOptions",
    "CoordKind",
    "Coord",
    "CartesianCoord",
    "CartesianGridOptions",
    "PolarCoord",
)


_dynamic_imports = {
    "BaseAxis": "axis",
    "CartesianAxis": "axis",
    "PolarAxis": "axis",
    "TickFormatter": "axis",
    "TickOptions": "axis",
    "CoordKind": "base",
    "Coord": "base",
    "CartesianCoord": "cartesian",
    "CartesianGridOptions": "options",
    "PolarCoord": "polar",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
