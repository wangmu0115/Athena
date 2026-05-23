from pydantic import Field

from athena_charts_matplotlib.styles.base import FontStyle, PaletteStyle, _BaseStyle
from athena_charts_matplotlib.styles.chart import ChartStyle
from athena_charts_matplotlib.styles.coord import AxisStyle, GridStyle, TickStyle
from athena_charts_matplotlib.styles.figure import FigureStyle
from athena_charts_matplotlib.styles.legend import LegendStyle
from athena_charts_matplotlib.styles.plot import LinePlotStyle


class MatplotlibStyle(_BaseStyle):
    """Matplotlib 全局样式，用于构建 `rcParams`。"""

    font: FontStyle | None = Field(None, description="字体")
    palette: PaletteStyle | None = Field(None, description="调色板")

    figure: FigureStyle | None = Field(None, description="画布")
    chart: ChartStyle | None = Field(None, description="图表")
    axis: AxisStyle | None = Field(None, description="坐标系-轴线")
    grid: GridStyle | None = Field(None, description="坐标系-网格")
    tick: TickStyle | None = Field(None, description="坐标系-刻度")
    legend: LegendStyle | None = Field(None, description="图例")
    line_plot: LinePlotStyle | None = Field(None, description="图层-折线&Marker")
