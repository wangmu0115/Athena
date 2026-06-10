from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.lark.models.sheets import (
        CreateSpreadsheetRequest,
        SheetsBatchUpdateRequest,
        SheetUpdateRequest,
        SheetWriteRequest,
    )

__all__ = (
    "CreateSpreadsheetRequest",
    "SheetUpdateRequest",
    "SheetsBatchUpdateRequest",
    "SheetWriteRequest",
)

_dynamic_imports = {
    "CreateSpreadsheetRequest": "sheets",
    "SheetUpdateRequest": "sheets",
    "SheetsBatchUpdateRequest": "sheets",
    "SheetWriteRequest": "sheets",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
