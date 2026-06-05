from typing import Self

from pydantic import Field

from athena_kit.matplotlib.styles.base import FontStyle, PaletteStyle, _BaseStyle
from athena_kit.matplotlib.styles.chart import ChartStyle
from athena_kit.matplotlib.styles.coord import AxisStyle
from athena_kit.matplotlib.styles.figure import FigureStyle
from athena_kit.matplotlib.styles.grid import GridStyle
from athena_kit.matplotlib.styles.legend import LegendStyle
from athena_kit.matplotlib.styles.plot import LinePlotStyle
from athena_kit.matplotlib.styles.presets.fonts import DEFAULT_FONT
from athena_kit.matplotlib.styles.presets.palettes import DEFAULT_PALETTE
from athena_kit.matplotlib.styles.tick import TickStyle


class Theme(_BaseStyle):
    """Matplotlib 全局样式，用于构建 `rcParams`。"""

    font: FontStyle | None = Field(None, description="字体")
    palette: PaletteStyle | None = Field(None, description="调色板")

    figure: FigureStyle | None = Field(None, description="画布")
    chart: ChartStyle | None = Field(None, description="图表")
    axis: AxisStyle | None = Field(None, description="坐标轴线")
    tick: TickStyle | None = Field(None, description="坐标轴的刻度，包括刻度线和刻度标签")
    grid: GridStyle | None = Field(None, description="网格")
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
            figure=figure or FigureStyle.of(),
            chart=chart or ChartStyle.of(),
            axis=axis or AxisStyle.of(),
            grid=grid or GridStyle.show(),
            tick=tick or TickStyle.of(),
            legend=legend or LegendStyle.of(),
            line_plot=line_plot or LinePlotStyle.of(),
        )
