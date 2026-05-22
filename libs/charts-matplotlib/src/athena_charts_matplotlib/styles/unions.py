from pydantic import Field

from athena_charts_matplotlib.styles._base import _BaseStyle
from athena_charts_matplotlib.styles.axes import MatplotlibAxesStyle
from athena_charts_matplotlib.styles.figure import MatplotlibFigureStyle
from athena_charts_matplotlib.styles.font import MatplotlibFontStyle
from athena_charts_matplotlib.styles.grid import MatplotlibGridStyle
from athena_charts_matplotlib.styles.palette import MatplotlibPaletteStyle


class MatplotlibStyle(_BaseStyle):
    """Matplotlib 全局样式，用于构建 `rcParams`。"""

    font: MatplotlibFontStyle | None = Field(None, description="字体配置")
    palette: MatplotlibPaletteStyle | None = Field(None, description="调色板")
    figure: MatplotlibFigureStyle | None = Field(None, description="画布配置")
    axes: MatplotlibAxesStyle | None = Field(None, description="Axes 配置")
    grid: MatplotlibGridStyle | None = Field(None, description="Grid 配置")


class MatplotlibAxesStyleOverride(_BaseStyle):
    """单个 `Axes` 的局部样式覆盖配置。"""

    axes: MatplotlibAxesStyle | None = Field(None, description="Axes 局部配置")
