from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_charts_matplotlib.styles.figure import MatplotlibFigureStyle
    from athena_charts_matplotlib.styles.font import MatplotlibFontStyle
    from athena_charts_matplotlib.styles.palette import MatplotlibPaletteStyle
    from athena_charts_matplotlib.styles.types import FontFamily
    from athena_charts_matplotlib.styles.unions import MatplotlibStyle


__all__ = (
    "MatplotlibFigureStyle",
    "MatplotlibStyle",
    "MatplotlibFontStyle",
    "MatplotlibPaletteStyle",
    "FontFamily",
)


_dynamic_imports = {
    "MatplotlibFigureStyle": "figure",
    "MatplotlibFontStyle": "font",
    "MatplotlibPaletteStyle": "palette",
    "FontFamily": "types",
    "MatplotlibStyle": "unions",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
