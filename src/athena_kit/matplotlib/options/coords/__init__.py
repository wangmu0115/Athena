from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.matplotlib.options.coords.axis import AxisLabelOptions, AxisOptions, AxisSpineOptions
    from athena_kit.matplotlib.options.coords.cartesian import CartesianCoordOptions
    from athena_kit.matplotlib.options.coords.grid import GridOptions
    from athena_kit.matplotlib.options.coords.legend import LegendOptions
    from athena_kit.matplotlib.options.coords.tick import TickLabelOptions, TickLineOptions, TickOptions


__all__ = (
    "AxisLabelOptions",
    "AxisOptions",
    "AxisSpineOptions",
    "TickLabelOptions",
    "TickLineOptions",
    "TickOptions",
    "GridOptions",
    "LegendOptions",
    "CartesianCoordOptions",
)


_dynamic_imports = {
    "AxisLabelOptions": "axis",
    "AxisOptions": "axis",
    "AxisSpineOptions": "axis",
    "TickLabelOptions": "tick",
    "TickLineOptions": "tick",
    "TickOptions": "tick",
    "GridOptions": "grid",
    "LegendOptions": "legend",
    "CartesianCoordOptions": "cartesian",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
