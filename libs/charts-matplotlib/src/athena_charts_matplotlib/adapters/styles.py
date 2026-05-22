from athena_charts.themes import FontWeight, LineStyle
from athena_core.values.optional import optional_map

_MPL_FONT_WEIGHT: dict[FontWeight, str] = {
    "ultralight": "ultralight",
    "light": "light",
    "normal": "normal",
    "medium": "medium",
    "semibold": "semibold",
    "bold": "bold",
    "heavy": "heavy",
    "black": "black",
}

_MPL_LINE_STYLE: dict[LineStyle, str] = {
    "solid": "-",
    "dashed": "--",
    "dotted": ":",
    "dashdot": "-.",
}


def to_mpl_font_weight(weight: FontWeight | None) -> str | None:
    return optional_map(weight, _MPL_FONT_WEIGHT.__getitem__)


def to_mpl_line_style(style: LineStyle | None) -> str | None:
    return optional_map(style, _MPL_LINE_STYLE.__getitem__)
