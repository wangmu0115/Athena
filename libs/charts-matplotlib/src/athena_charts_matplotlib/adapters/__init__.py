from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_charts_matplotlib.adapters.styles import (
        to_mpl_font_weight,
        to_mpl_line_style,
    )


__all__ = (
    "to_mpl_font_weight",
    "to_mpl_line_style",
)


_dynamic_imports = {
    "to_mpl_font_weight": "styles",
    "to_mpl_line_style": "styles",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
