from pydantic import Field

from athena_matplotlib.options._base import _BaseOptions
from athena_matplotlib.options.axis import AxisOptions
from athena_matplotlib.options.grid import GridOptions
from athena_matplotlib.options.tick import TickOptions


class CartesianCoordOptions(_BaseOptions):
    top_axis: AxisOptions | None = Field(None, description="Top X 轴轴线和标题配置项")
    bottom_axis: AxisOptions | None = Field(None, description="Bottom X 轴轴线和标题配置项")
    left_axis: AxisOptions | None = Field(None, description="Left Y 轴轴线和标题配置项")
    right_axis: AxisOptions | None = Field(None, description="Right Y 轴轴线和标题配置项")

    top_tick: TickOptions | None = Field(None, description="Top X 轴刻度线配置项")
    bottom_tick: TickOptions | None = Field(None, description="Bottom X 轴刻度线配置项")
    left_tick: TickOptions | None = Field(None, description="Left Y 轴刻度线配置项")
    right_tick: TickOptions | None = Field(None, description="Right Y 轴刻度线配置项")

    grid: GridOptions | None = Field(None, description="网格线配置")
