from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_charts.specs.rules.conditions import (
        DataCondition,
        DataField,
        DataPredicate,
    )
    from athena_charts.specs.rules.styles import (
        DataLabelStyleRule,
        MarkerStyleRule,
        StyleRule,
    )


__all__ = (
    "DataField",
    "DataPredicate",
    "DataCondition",
    "StyleRule",
    "DataLabelStyleRule",
    "MarkerStyleRule",
)


_dynamic_imports = {
    "DataField": "conditions",
    "DataCondition": "conditions",
    "DataPredicate": "conditions",
    "StyleRule": "styles",
    "DataLabelStyleRule": "styles",
    "MarkerStyleRule": "styles",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
