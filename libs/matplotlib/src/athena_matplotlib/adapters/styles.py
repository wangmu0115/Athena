from athena_matplotlib.types import LegendLocation, LineStyle, MarkerShape

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


def to_mpl_line_style(line_style: LineStyle | None) -> str:
    if line_style is None:
        return "solid"
    return _MPL_LINE_STYLE.get(line_style)


def to_mpl_legend_loc(loc: LegendLocation | None) -> str | None:
    if loc is None:
        return "best"
    return _MPL_LEGEND_LOC.get(loc)


def to_mpl_marker_shape(marker: MarkerShape | None) -> str | None:
    if marker is None:
        return "o"
    return _MPL_MARKER_SHAPE.get(marker)
