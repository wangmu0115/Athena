from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.core.tabular.backend import TableBackend, TableLocator
    from athena_kit.core.tabular.dataframe import dataframe_to_models, models_to_dataframe, table_rows_to_dataframe
    from athena_kit.core.tabular.fields import SourceField, TableField
    from athena_kit.core.tabular.repository import TableRepository
    from athena_kit.core.tabular.schema import BaseTableRow
    from athena_kit.core.tabular.serialization import deserialize_cell_value, serialize_cell_value

__all__ = (
    "TableLocator",
    "TableBackend",
    "serialize_cell_value",
    "deserialize_cell_value",
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
    "serialize_cell_value": "serialization",
    "deserialize_cell_value": "serialization",
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
