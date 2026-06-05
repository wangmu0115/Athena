from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_core.tabular.backend import TableBackend, TableLocator
    from athena_core.tabular.codec import decode_cell_value, encode_field_value
    from athena_core.tabular.dataframe import dataframe_to_models, models_to_dataframe, table_rows_to_dataframe
    from athena_core.tabular.fields import SourceField, TableField
    from athena_core.tabular.repository import TableRepository
    from athena_core.tabular.schema import BaseTableRow

__all__ = (
    "TableLocator",
    "TableBackend",
    "encode_field_value",
    "decode_cell_value",
    "TableField",
    "SourceField",
    "BaseTableRow",
    "TableRepository",
    "dataframe_to_models",
    "models_to_dataframe",
    "table_rows_to_dataframe",
)

_dynamic_imports = {
    "TableLocator": "backend",
    "TableBackend": "backend",
    "encode_field_value": "codec",
    "decode_cell_value": "codec",
    "TableField": "fields",
    "SourceField": "fields",
    "BaseTableRow": "schema",
    "TableRepository": "repository",
    "dataframe_to_models": "dataframe",
    "models_to_dataframe": "dataframe",
    "table_rows_to_dataframe": "dataframe",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
