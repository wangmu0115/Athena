from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.lark.aclient import AsyncLarkClient
    from athena_kit.lark.auth import LarkTenantAccessTokenAuth

__all__ = (
    "AsyncLarkClient",
    "LarkTenantAccessTokenAuth",
)

_dynamic_imports = {
    "AsyncLarkClient": "aclient",
    "LarkTenantAccessTokenAuth": "auth",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
