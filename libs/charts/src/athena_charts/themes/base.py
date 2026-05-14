from pydantic import Field

from athena_charts.themes import (
    AxisTheme,
    ChartTheme,
    FigureTheme,
    GridTheme,
    LegendTheme,
    PlotTheme,
)
from athena_core.models import BaseAthenaModel


class TextTheme(BaseAthenaModel):
    color: str = Field("#111111", description="默认文本颜色")
    font_family: str = Field("sans-serif", description="图表默认字体族")
    sans_serif_fonts: list[str] = Field(
        default_factory=lambda: [
            "Hiragino Sans GB",
            "Arial Unicode MS",
            "PingFang SC",
            "Noto Sans CJK SC",
            "Microsoft YaHei",
            "SimHei",
            "DejaVu Sans",
            "sans-serif",
        ]
    )


class PaletteTheme(BaseAthenaModel):
    colors: list[str] = Field(
        default_factory=lambda: [
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
        ],
        description="默认颜色调色板",
    )

    def pick(self, index: int) -> str | None:
        if not self.colors:
            return None
        return self.colors[index % len(self.colors)]


class Theme(BaseAthenaModel):
    text: TextTheme = Field(default_factory=TextTheme, description="全局文本主题")
    palette: PaletteTheme = Field(default_factory=PaletteTheme, description="调色板主题")

    figure: FigureTheme = Field(default_factory=FigureTheme, description="画布主题")
    chart: ChartTheme = Field(default_factory=ChartTheme, description="图表主题")
    axis: AxisTheme = Field(default_factory=AxisTheme, description="坐标轴主题")
    grid: GridTheme = Field(default_factory=GridTheme, description="网格主题")
    legend: LegendTheme = Field(default_factory=LegendTheme, description="图例主题")
    plot: PlotTheme = Field(default_factory=PlotTheme, description="图层主题")


DEFAULT_THEME = Theme()
