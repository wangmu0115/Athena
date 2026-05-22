from athena_charts.themes.chart import ChartTheme
from athena_charts.themes.coord import AxisTheme, GridTheme, TickTheme
from athena_charts.themes.figure import FigureTheme
from athena_charts.themes.legend import LegendTheme
from athena_charts.themes.plot import PlotTheme
from athena_charts.themes.presets.fonts import DEFAULT_FONT_THEME
from athena_charts.themes.presets.palettes import DEFAULT_PALETTE_THEME
from athena_charts.themes.unions import Theme

DEFAULT_THEME = Theme(
    font=DEFAULT_FONT_THEME,
    palette=DEFAULT_PALETTE_THEME,
    figure=FigureTheme(
        background_color="white",
        edge_color="white",
        edge_linewidth=0.8,
        title_fontsize=12,
        title_fontweight="bold",
        title_color="#111111",
        subtitle_fontsize=10,
        subtitle_fontweight="normal",
        subtitle_color="#5d5b5b",
    ),
    chart=ChartTheme(
        background_color="white",
        edge_color="white",
        edge_linewidth=0.8,
        title_fontsize=12,
        title_fontweight="bold",
        title_color="#111111",
        subtitle_fontsize=10,
        subtitle_fontweight="normal",
        subtitle_color="#5d5b5b",
    ),
    axis=AxisTheme(
        line_color="#333333",
        line_width=0.8,
        label_fontsize=8,
        label_fontweight="normal",
        label_color="#111111",
    ),
    tick=TickTheme(
        tick_color="#333333",
        tick_width=0.1,
        tick_length=0.2,
        tick_direction="out",
        label_fontsize=6,
        label_fontweight="normal",
        label_color="#111111",
        label_rotation=0,
    ),
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
    plot=PlotTheme(
        opacity=1.0,
        line_width=1.0,
        line_style="solid",
        marker_size=0.3,
        marker_edgecolor=None,
        marker_edgewidth=None,
        bar_width=0.2,
        bar_edgecolor=None,
        bar_edgewidth=None,
    ),
)
