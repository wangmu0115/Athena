from pydantic import Field

from athena_charts.themes._base import _BaseTheme
from athena_charts.themes.chart import ChartTheme
from athena_charts.themes.coord import AxisTheme, GridTheme, TickTheme
from athena_charts.themes.figure import FigureTheme
from athena_charts.themes.font import FontTheme
from athena_charts.themes.legend import LegendTheme
from athena_charts.themes.palette import PaletteTheme
from athena_charts.themes.plot import PlotTheme


class Theme(_BaseTheme):
    font: FontTheme = Field(default_factory=FontTheme, description="全局文本主题")
    palette: PaletteTheme = Field(default_factory=PaletteTheme, description="调色板主题")
    figure: FigureTheme = Field(default_factory=FigureTheme, description="画布主题")
    chart: ChartTheme = Field(default_factory=ChartTheme, description="图表主题")
    axis: AxisTheme = Field(default_factory=AxisTheme, description="坐标轴主题")
    tick: TickTheme = Field(default_factory=TickTheme, description="刻度线主题")
    grid: GridTheme = Field(default_factory=GridTheme, description="网格主题")
    legend: LegendTheme = Field(default_factory=LegendTheme, description="图例主题")
    plot: PlotTheme = Field(default_factory=PlotTheme, description="图层主题")
