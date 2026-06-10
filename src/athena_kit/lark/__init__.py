from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.lark.auth import LarkTenantAccessTokenAuth, LarkTenantTokenOptions
    from athena_kit.lark.client import LarkClient
    from athena_kit.lark.config import LarkConfig, LarkSheetLocatorConfig
    from athena_kit.lark.validators import LARK_SUCCESS_VALIDATOR

__all__ = (
    "LarkTenantAccessTokenAuth",
    "LarkTenantTokenOptions",
    "LARK_SUCCESS_VALIDATOR",
    "LarkClient",
    "LarkConfig",
    "LarkSheetLocatorConfig",
)

_dynamic_imports = {
    "LarkTenantAccessTokenAuth": "auth",
    "LarkTenantTokenOptions": "auth",
    "LARK_SUCCESS_VALIDATOR": "validators",
    "LarkClient": "client",
    "LarkConfig": "config",
    "LarkSheetLocatorConfig": "config",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
