from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_matplotlib.options.cartesian import CartesianCoordOptions
    from athena_matplotlib.options.chart import ChartOptions
    from athena_matplotlib.options.renderfig import RenderFigureOptions
    from athena_matplotlib.options.savefig import PngExportStyle, SaveFigureOptions


__all__ = (
    "PngExportStyle",
    "SaveFigureOptions",
    "RenderFigureOptions",
    "ChartOptions",
    "CartesianCoordOptions",
)


_dynamic_imports = {
    "PngExportStyle": "savefig",
    "SaveFigureOptions": "savefig",
    "RenderFigureOptions": "renderfig",
    "ChartOptions": "chart",
    "CartesianCoordOptions": "cartesian",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
