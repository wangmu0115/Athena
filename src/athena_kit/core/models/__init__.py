from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.core.models.base import BaseAthenaModel
    from athena_kit.core.models.enums import LabelIntEnum, LabelStrEnum
    from athena_kit.core.models.mapping import model_to_model, models_to_model

__all__ = (
    "BaseAthenaModel",
    "LabelIntEnum",
    "LabelStrEnum",
    "model_to_model",
    "models_to_model",
)

_dynamic_imports = {
    "BaseAthenaModel": "base",
    "LabelIntEnum": "enums",
    "LabelStrEnum": "enums",
    "model_to_model": "mapping",
    "models_to_model": "mapping",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
