from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.matplotlib.specs.coords.base import AxisSpec, Coord
    from athena_kit.matplotlib.specs.coords.cartesian import CartesianAxisSpec, CartesianCoord
    from athena_kit.matplotlib.specs.coords.polar import PolarAxisSpec, PolarCoord
    from athena_kit.matplotlib.specs.coords.tick import TickLabelFormatter, TickLocator, TickSpec
    from athena_kit.matplotlib.specs.coords.unions import CoordSpec


__all__ = (
    "AxisSpec",
    "Coord",
    "CoordSpec",
    "CartesianAxisSpec",
    "CartesianCoord",
    "PolarAxisSpec",
    "PolarCoord",
    "TickLabelFormatter",
    "TickLocator",
    "TickSpec",
)


_dynamic_imports = {
    "AxisSpec": "base",
    "Coord": "base",
    "CoordSpec": "unions",
    "CartesianAxisSpec": "cartesian",
    "CartesianCoord": "cartesian",
    "PolarAxisSpec": "polar",
    "PolarCoord": "polar",
    "TickLabelFormatter": "tick",
    "TickLocator": "tick",
    "TickSpec": "tick",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
