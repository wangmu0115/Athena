from typing import Self

from pydantic import Field

from athena_charts_matplotlib.styles.base import FontStyle, PaletteStyle, _BaseStyle
from athena_charts_matplotlib.styles.chart import ChartStyle
from athena_charts_matplotlib.styles.coord import AxisStyle, GridStyle, TickStyle
from athena_charts_matplotlib.styles.figure import FigureStyle
from athena_charts_matplotlib.styles.legend import LegendStyle
from athena_charts_matplotlib.styles.plot import LinePlotStyle
from athena_charts_matplotlib.styles.presets import DEFAULT_FONT, DEFAULT_PALETTE


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

    @classmethod
    def default(cls) -> Self:
        return cls.of()

    @classmethod
    def of(
        cls,
        font: FontStyle | None = None,
        palette: PaletteStyle | None = None,
        figure: FigureStyle | None = None,
        chart: ChartStyle | None = None,
        axis: AxisStyle | None = None,
        grid: GridStyle | None = None,
        tick: TickStyle | None = None,
        legend: LegendStyle | None = None,
        line_plot: LinePlotStyle | None = None,
    ) -> Self:
        return cls(
            font=font or DEFAULT_FONT,
            palette=palette or DEFAULT_PALETTE,
            figure=figure or FigureStyle.default(),
            chart=chart or ChartStyle.default(),
            axis=axis or AxisStyle.default(),
            grid=grid or GridStyle.default(),
            tick=tick or TickStyle.default(),
            legend=legend or LegendStyle.default(),
            line_plot=line_plot or LinePlotStyle.default(),
        )
