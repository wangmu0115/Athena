from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.lark.sheets.aclient import LarkSheetsAsyncClient
    from athena_kit.lark.sheets.backend import AsyncLarkSheetsBackend, LarkSheetsLocator

__all__ = (
    "LarkSheetsAsyncClient",
    "LarkSheetsLocator",
    "AsyncLarkSheetsBackend",
)

_dynamic_imports = {
    "LarkSheetsAsyncClient": "aclient",
    "LarkSheetsLocator": "backend",
    "AsyncLarkSheetsBackend": "backend",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
