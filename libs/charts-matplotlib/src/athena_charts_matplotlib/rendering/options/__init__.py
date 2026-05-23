from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_charts_matplotlib.rendering.options.base import (
        ColorCycle,
    )
    from athena_charts_matplotlib.rendering.options.savefig import PngExportStyle, SaveFigureOptions
    from athena_charts_matplotlib.rendering.options.unions import MatplotlibRenderOptions


__all__ = (
    "ColorCycle",
    "PngExportStyle",
    "SaveFigureOptions",
    "MatplotlibRenderOptions",
)


_dynamic_imports = {
    "ColorCycle": "base",
    "PngExportStyle": "savefig",
    "SaveFigureOptions": "savefig",
    "MatplotlibRenderOptions": "unions",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
