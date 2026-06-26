from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.lark.bitables.aclient import LarkBitablesAsyncClient
    from athena_kit.lark.bitables.field_client import LarkBitableFieldsAsyncClient
    from athena_kit.lark.bitables.models import BitableField, BitableRecord
    from athena_kit.lark.bitables.record_client import LarkBitableRecordsAsyncClient

__all__ = (
    "LarkBitablesAsyncClient",
    "LarkBitableRecordsAsyncClient",
    "LarkBitableFieldsAsyncClient",
    "BitableRecord",
    "BitableField",
)

_dynamic_imports = {
    "LarkBitablesAsyncClient": "aclient",
    "LarkBitableRecordsAsyncClient": "record_client",
    "LarkBitableFieldsAsyncClient": "field_client",
    "BitableRecord": "models",
    "BitableField": "models",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
