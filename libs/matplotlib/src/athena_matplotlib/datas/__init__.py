from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_matplotlib.datas.categorical import CategoricalDatum, CategoricalSeriesData
    from athena_matplotlib.datas.xy import XYPoint, XYSeriesData


__all__ = (
    "XYPoint",
    "XYSeriesData",
    "CategoricalDatum",
    "CategoricalSeriesData",
)


_dynamic_imports = {
    "XYPoint": "xy",
    "XYSeriesData": "xy",
    "CategoricalDatum": "categorical",
    "CategoricalSeriesData": "categorical",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
