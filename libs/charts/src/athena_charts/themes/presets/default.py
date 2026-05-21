from athena_charts.themes.chart import ChartTheme
from athena_charts.themes.coord import AxisTheme, GridTheme, TickTheme
from athena_charts.themes.figure import FigureTheme
from athena_charts.themes.font import FontTheme
from athena_charts.themes.legend import LegendTheme
from athena_charts.themes.palette import PaletteTheme
from athena_charts.themes.unions import Theme

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
    fallbacks=["Hiragino Sans GB", "Arial Unicode MS", "PingFang SC", "Noto Sans CJK SC", "Microsoft YaHei"],
    color="#111111",
    weight="normal",
)

DEFAULT_PALETTE_THEME = PaletteTheme(
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

DEFAULT_FIGURE_THEME = FigureTheme(
    background_color="white",
    edge_color="white",
    edge_linewidth=0.8,
    title_fontsize=12,
    title_fontweight="bold",
    title_color="#111111",
    subtitle_fontsize=10,
    subtitle_fontweight="normal",
    subtitle_color="#5d5b5b",
)

DEFAULT_CHART_THEME = ChartTheme(
    background_color="white",
    edge_color="white",
    edge_linewidth=0.8,
    title_fontsize=12,
    title_fontweight="bold",
    title_color="#111111",
    subtitle_fontsize=10,
    subtitle_fontweight="normal",
    subtitle_color="#5d5b5b",
)

DEFAULT_AXIS_THEME = AxisTheme(
    line_color="#333333",
    line_width=0.8,
    label_fontsize=8,
    label_fontweight="normal",
    label_color="#111111",
)

DEFAULT_TICK_THEME = TickTheme(
    tick_color="#333333",
    tick_width=0.1,
    tick_length=0.2,
    tick_direction="out",
    label_fontsize=6,
    label_fontweight="normal",
    label_color="#111111",
    label_rotation=0,
)

DEFAULT_THEME = Theme(
    font=DEFAULT_FONT_THEME,
    palette=DEFAULT_PALETTE_THEME,
    figure=DEFAULT_FIGURE_THEME,
    chart=DEFAULT_CHART_THEME,
    axis=DEFAULT_AXIS_THEME,
    tick=DEFAULT_TICK_THEME,
    grid=GridTheme(line_color="#999999", line_width=0.25, line_style="solid", alpha=0.25),
    legend=LegendTheme(
        location="auto",
        direction="vertical",
        title_fontsize=6,
        title_fontweight="normal",
        title_color="#111111",
        label_fontsize=4,
        label_fontweight="light",
        label_color="#111111",
        background_color="white",
        edge_color="#333333",
        edge_width=0.05,
        alpha=0.8,
    ),
)
