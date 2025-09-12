from typing import TYPE_CHECKING

from _import_utils import import_attr

if TYPE_CHECKING:
    from standard import parse_str_date

__all__ = [
    "parse_str_date",
]

_dynamic_imports = {
    "parse_str_date": "standard",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return __all__
