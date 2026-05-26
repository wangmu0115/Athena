from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_matplotlib.types.options import (
        BboxInches,
        ImageFormat,
    )
    from athena_matplotlib.types.specs import (
        AxisDataType,
        BarLayoutMode,
        CartesianAxisPosition,
        CoordKind,
        PlotKind,
        PolarAxisRole,
        TickLabelFormatKind,
        TickLocatorStrategy,
    )
    from athena_matplotlib.types.styles import (
        AxisScale,
        FontFamily,
        FontWeight,
        GridAxis,
        HorizontalAlignment,
        LegendLocation,
        LineStyle,
        MarkerShape,
        TickDirection,
        VerticalAlignment,
    )

__all__ = (
    "AxisScale",
    "FontFamily",
    "FontWeight",
    "TickDirection",
    "GridAxis",
    "LegendLocation",
    "LineStyle",
    "MarkerShape",
    "HorizontalAlignment",
    "VerticalAlignment",
    "ImageFormat",
    "BboxInches",
    "AxisDataType",
    "BarLayoutMode",
    "CartesianAxisPosition",
    "CoordKind",
    "PlotKind",
    "PolarAxisRole",
    "TickLabelFormatKind",
    "TickLocatorStrategy",
)


_dynamic_imports = {
    "AxisScale": "styles",
    "FontFamily": "styles",
    "FontWeight": "styles",
    "TickDirection": "styles",
    "GridAxis": "styles",
    "LegendLocation": "styles",
    "LineStyle": "styles",
    "MarkerShape": "styles",
    "HorizontalAlignment": "styles",
    "VerticalAlignment": "styles",
    "ImageFormat": "options",
    "BboxInches": "options",
    "AxisDataType": "specs",
    "BarLayoutMode": "specs",
    "CartesianAxisPosition": "specs",
    "CoordKind": "specs",
    "PlotKind": "specs",
    "PolarAxisRole": "specs",
    "TickLabelFormatKind": "specs",
    "TickLocatorStrategy": "specs",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
