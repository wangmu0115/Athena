from typing import TYPE_CHECKING

from athena_kit._import_utils import import_attr

if TYPE_CHECKING:
    from athena_kit.matplotlib.rendering.plots.layers.datalabel_layer import DataLabelLayerArtist
    from athena_kit.matplotlib.rendering.plots.layers.line_layer import LineLayerArtist
    from athena_kit.matplotlib.rendering.plots.layers.marker_layer import MarkerLayerArtist


__all__ = (
    "LineLayerArtist",
    "MarkerLayerArtist",
    "DataLabelLayerArtist",
)


_dynamic_imports = {
    "LineLayerArtist": "line_layer",
    "MarkerLayerArtist": "marker_layer",
    "DataLabelLayerArtist": "datalabel_layer",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
