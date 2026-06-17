from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.core import models, tabular, temporal, values

__all__ = (
    "models",
    "tabular",
    "temporal",
    "values",
)

_dynamic_imports = {
    "models": "__module__",
    "tabular": "__module__",
    "temporal": "__module__",
    "values": "__module__",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
