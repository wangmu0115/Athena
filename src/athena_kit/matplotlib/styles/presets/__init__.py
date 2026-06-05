from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.matplotlib.styles.presets.fonts import DEFAULT_FONT
    from athena_kit.matplotlib.styles.presets.palettes import DEFAULT_PALETTE


__all__ = (
    "DEFAULT_FONT",
    "DEFAULT_PALETTE",
)


_dynamic_imports = {
    "DEFAULT_FONT": "fonts",
    "DEFAULT_PALETTE": "palettes",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
