from athena_charts.themes.base import (
    AxisTheme,
    ChartTheme,
    GridTheme,
    LegendTheme,
    PaletteTheme,
    PlotTheme,
    Theme,
)
from athena_charts.themes.figure import FigureTheme
from athena_charts.themes.font import FontTheme

DEFAULT_THEME_1 = Theme(
    font=FontTheme(
        color="#111111",
        font_family="sans-serif",
        sans_serif_fonts=[
            "Hiragino Sans GB",
            "Arial Unicode MS",
            "PingFang SC",
            "Noto Sans CJK SC",
            "Microsoft YaHei",
            "SimHei",
            "DejaVu Sans",
            "sans-serif",
        ],
    ),
    palette=PaletteTheme(
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
    ),
    figure=FigureTheme(
        width=800,
        height=480,
        background_color="white",
        title_font_size=13,
        subtitle_font_size=11,
    ),
    chart=ChartTheme(
        background_color="white",
        title_font_size=13,
        subtitle_font_size=11,
    ),
    axis=AxisTheme(
        edge_color="#333333",
        label_color="#111111",
        label_font_size=10,
        tick_color="#333333",
        tick_font_size=8,
    ),
    grid=GridTheme(
        visible=True,
        color="#999999",
        alpha=0.25,
        line_width=0.5,
    ),
    legend=LegendTheme(
        visible=True,
        title_font_size=10,
        font_size=8,
    ),
    plot=PlotTheme(
        opacity=1.0,
        line_width=1.5,
        marker_size=3.0,
        bar_width=0.8,
    ),
)

DEFAULT_FONT_THEME = FontTheme(
    family="sans-serif",
    fallbacks=[
        "Hiragino Sans GB",
        "Arial Unicode MS",
        "PingFang SC",
        "Noto Sans CJK SC",
        "Microsoft YaHei",
        "SimHei",
        "DejaVu Sans",
    ],
    color="#111111",
    wight="normal",
)

DEFAULT_FIGURE_THEME = FigureTheme(
    background_color="white",
    edge_color="white",
    title_font_size=14,
    subtitle_font_size=12,
    title_font_weight="normal",
)


DEFAULT_THEME = Theme(
    font=DEFAULT_FONT_THEME,
    figure=DEFAULT_FIGURE_THEME,
)
