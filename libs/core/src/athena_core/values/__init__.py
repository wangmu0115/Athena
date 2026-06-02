from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_core.values.fallbacks import (
        first_non_empty,
        first_not_none,
        first_truthy,
    )
    from athena_core.values.optional import (
        optional_map,
        optional_map_or,
        optional_map_or_else,
        optional_or,
        optional_or_else,
        safe_getattr,
    )

__all__ = (
    "first_non_empty",
    "first_not_none",
    "first_truthy",
    "optional_map",
    "optional_map_or",
    "optional_map_or_else",
    "optional_or",
    "optional_or_else",
    "safe_getattr",
)

_dynamic_imports = {
    "first_non_empty": "fallbacks",
    "first_not_none": "fallbacks",
    "first_truthy": "fallbacks",
    "optional_map": "optional",
    "optional_map_or": "optional",
    "optional_map_or_else": "optional",
    "optional_or": "optional",
    "optional_or_else": "optional",
    "safe_getattr": "optional",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
