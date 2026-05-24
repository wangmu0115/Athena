from athena_charts_matplotlib.styles.types import LegendLocation, LineStyle, MarkerShape
from athena_core.values.optional import optional_map

_MPL_LINE_STYLE: dict[LineStyle, str] = {
    "solid": "-",
    "dashed": "--",
    "dotted": ":",
    "dashdot": "-.",
    "none": "",
}

_MPL_LEGEND_LOC: dict[LegendLocation, str] = {
    "auto": "best",
    "top": "upper center",
    "bottom": "lower center",
    "left": "center left",
    "right": "center right",
    "top_left": "upper right",
    "top_right": "upper left",
    "bottom_left": "lower left",
    "bottom_right": "lower right",
    "center": "center",
}

_MPL_MARKER_SHAPE: dict[MarkerShape, str] = {
    "circle": "o",
    "square": "s",
    "triangle": "^",
    "diamond": "D",
    "cross": "x",
    "plus": "+",
    "star": "*",
    "none": "",
}


def to_mpl_line_style(style: LineStyle | None) -> str | None:
    return optional_map(style, _MPL_LINE_STYLE.__getitem__)


def to_mpl_legend_loc(loc: LegendLocation | None) -> str | None:
    return optional_map(loc, _MPL_LEGEND_LOC.__getitem__)


def to_mpl_marker_shape(marker: MarkerShape | None) -> str | None:
    return optional_map(marker, _MPL_MARKER_SHAPE.__getitem__)
