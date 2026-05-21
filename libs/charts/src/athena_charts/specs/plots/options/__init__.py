from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_charts.specs.plots.options.labels import DataLabelOptions
    from athena_charts.specs.plots.options.markers import MarkerOptions


__all__ = (
    "DataLabelOptions",
    "MarkerOptions",
)


_dynamic_imports = {
    "DataLabelOptions": "labels",
    "MarkerOptions": "markers",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
