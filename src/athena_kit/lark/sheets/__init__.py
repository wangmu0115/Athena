from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.lark.sheets.aclient import LarkSheetsAsyncClient
    from athena_kit.lark.sheets.backend import LarkSheetBackend, LarkSheetLocator
    from athena_kit.lark.sheets.validators import SHEETS_SUCCESS_VALIDATOR

__all__ = (
    "LarkSheetsAsyncClient",
    "LarkSheetLocator",
    "LarkSheetBackend",
    "SHEETS_SUCCESS_VALIDATOR",
)

_dynamic_imports = {
    "LarkSheetsAsyncClient": "aclient",
    "LarkSheetLocator": "backend",
    "LarkSheetBackend": "backend",
    "SHEETS_SUCCESS_VALIDATOR": "validators",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
