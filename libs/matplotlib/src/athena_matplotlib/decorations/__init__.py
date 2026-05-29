from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_matplotlib.decorations.axis import apply_axis_style
    from athena_matplotlib.decorations.cartesian import apply_cartesian_style
    from athena_matplotlib.decorations.chart import apply_chart_style
    from athena_matplotlib.decorations.grid import apply_grid_style
    from athena_matplotlib.decorations.tick import apply_tick_style


__all__ = (
    "apply_chart_style",
    "apply_axis_style",
    "apply_cartesian_style",
    "apply_grid_style",
    "apply_tick_style",
)


_dynamic_imports = {
    "apply_axis_style": "axis",
    "apply_chart_style": "chart",
    "apply_cartesian_style": "cartesian",
    "apply_grid_style": "grid",
    "apply_tick_style": "tick",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
