from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.lark.sheets.aclient import LarkSheetsAsyncClient
    from athena_kit.lark.sheets.backend import LarkSheetBackend, LarkSheetLocator

__all__ = (
    "LarkSheetsAsyncClient",
    "LarkSheetLocator",
    "LarkSheetBackend",
)

_dynamic_imports = {
    "LarkSheetsAsyncClient": "aclient",
    "LarkSheetLocator": "backend",
    "LarkSheetBackend": "backend",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
