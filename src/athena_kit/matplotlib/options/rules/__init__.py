from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.matplotlib.options.rules.conditions import (
        DataCondition,
        DataPredicate,
    )
    from athena_kit.matplotlib.options.rules.data_context import DataContext, DataField
    from athena_kit.matplotlib.options.rules.matches import match_data_condition, match_data_predicate


__all__ = (
    "DataPredicate",
    "DataCondition",
    "DataField",
    "DataContext",
    "match_data_condition",
    "match_data_predicate",
)


_dynamic_imports = {
    "DataCondition": "conditions",
    "DataPredicate": "conditions",
    "DataField": "data_context",
    "DataContext": "data_context",
    "match_data_condition": "matches",
    "match_data_predicate": "matches",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
