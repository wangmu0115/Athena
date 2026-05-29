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
    """将 Athena 线型枚举转换为 Matplotlib 线型字符串，当传入 `None` 时，默认返回 `solid`。

    Notes:
        - solid -> "-"
        - dashed -> "--"
        - dotted -> ":"
        - dashdot -> "-."
        - none -> "" # 不显示 line
    """
    if line_style is None:
        return "solid"
    return _MPL_LINE_STYLE[line_style]


def to_mpl_legend_loc(loc: LegendLocation | None) -> str:
    """将 Athena 图例位置枚举转换为 Matplotlib legend loc 参数，当传入 `None` 时，默认返回 `best`。

    Notes:
        - auto -> best
        - top -> upper center
        - bottom -> lower center
        - left -> center left
        - right -> center right
        - top_left -> upper left
        - top_right -> upper right
        - bottom_left -> lower left
        - bottom_right -> lower right
        - center -> center
    """
    if loc is None:
        return "best"
    return _MPL_LEGEND_LOC[loc]


def to_mpl_marker_shape(marker: MarkerShape | None) -> str | None:
    """将 Athena Marker 形状枚举转换为 Matplotlib Marker 字符串，当传入 `None` 时，默认返回 `o`。

    Notes:
        - circle -> "o"
        - square -> "s"
        - triangle -> "^"
        - diamond -> "D"
        - cross -> "x"
        - plus -> "+"
        - star -> "*"
        - none -> "" # 不显示 marker
    """
    if marker is None:
        return "o"
    return _MPL_MARKER_SHAPE[marker]
