from athena_charts_matplotlib.options.base import MatplotlibOptions, MatplotlibPaletteOptions
from athena_charts_matplotlib.options.figure import MatplotlibFigureOptions
from athena_charts_matplotlib.options.font import MatplotlibFontOptions
from athena_charts_matplotlib.options.saving import MatplotlibSavingOptions

DEFAULT_PALETTE_OPTIONS = MatplotlibPaletteOptions(
    sequence=[
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
    ]
)

DEFAULT_FONT_OPTIONS = MatplotlibFontOptions(
    family="sans-serif",
    fonts=[
        "Hiragino Sans GB",
        "Arial Unicode MS",
        "PingFang SC",
        "Noto Sans CJK SC",
        "Microsoft YaHei",
        "SimHei",
        "DejaVu Sans",
        "sans-serif",
    ],
    color="#111111",
    weight="normal",
)

DEFAULT_FIGURE_OPTIONS = MatplotlibFigureOptions(
    width=1280,
    height=960,
    dpi=200,
    facecolor="white",
    edgecolor="white",
    titlesize=14,
    titleweight="normal",
)

DEFAULT_SAVING_OPTIONS = MatplotlibSavingOptions(
    dpi=200,
    format="png",
    bbox_inches="tight",
    pad_inches=0.1,
    transparent=False,
)


DEFAULT_MATPLOTLIB_OPTIONS = MatplotlibOptions(
    palette=DEFAULT_PALETTE_OPTIONS,
    font=DEFAULT_FONT_OPTIONS,
    figure=DEFAULT_FIGURE_OPTIONS,
    saving=DEFAULT_SAVING_OPTIONS,
)
