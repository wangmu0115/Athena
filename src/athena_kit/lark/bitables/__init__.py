from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.lark.bitables.aclient import LarkBitablesAsyncClient
    from athena_kit.lark.bitables.fields import LarkBitableFieldsAsyncClient
    from athena_kit.lark.bitables.models import BitableField, BitableFieldType, BitableFieldUiType, BitableRecord
    from athena_kit.lark.bitables.records import LarkBitableRecordsAsyncClient

__all__ = (
    "LarkBitablesAsyncClient",
    "LarkBitableRecordsAsyncClient",
    "LarkBitableFieldsAsyncClient",
    "BitableRecord",
    "BitableField",
    "BitableFieldType",
    "BitableFieldUiType",
)

_dynamic_imports = {
    "LarkBitablesAsyncClient": "aclient",
    "LarkBitableRecordsAsyncClient": "records",
    "LarkBitableFieldsAsyncClient": "fields",
    "BitableRecord": "models",
    "BitableField": "models",
    "BitableFieldType": "models",
    "BitableFieldUiType": "models",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
