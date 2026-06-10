from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.lark.aclient import AsyncLarkClient
    from athena_kit.lark.auth import LarkTenantAccessTokenAuth
    from athena_kit.lark.config import LarkConfig, LarkSheetLocatorConfig

__all__ = (
    "AsyncLarkClient",
    "LarkTenantAccessTokenAuth",
    "LarkConfig",
    "LarkSheetLocatorConfig",
)

_dynamic_imports = {
    "AsyncLarkClient": "aclient",
    "LarkTenantAccessTokenAuth": "auth",
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
