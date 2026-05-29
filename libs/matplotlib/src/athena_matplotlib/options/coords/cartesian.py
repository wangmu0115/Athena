from typing import Self

from pydantic import Field

from athena_matplotlib.options._base import _BaseOptions
from athena_matplotlib.options.coords.axis import AxisOptions
from athena_matplotlib.options.coords.grid import GridOptions
from athena_matplotlib.options.coords.legend import LegendOptions
from athena_matplotlib.options.coords.tick import TickOptions


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
    legend: LegendOptions | None = Field(None, description="图例配置")

    @classmethod
    def of(cls, *, grid: GridOptions | None = None, legend: LegendOptions | None = None) -> Self:
        return cls(grid=grid, legend=legend)

    def top(self, *, axis: AxisOptions | None = None, tick: TickOptions | None) -> Self:
        self.top_axis = axis
        self.top_tick = tick
        return self

    def bottom(self, *, axis: AxisOptions | None = None, tick: TickOptions | None) -> Self:
        self.bottom_axis = axis
        self.bottom_tick = tick
        return self

    def left(self, *, axis: AxisOptions | None = None, tick: TickOptions | None) -> Self:
        self.left_axis = axis
        self.left_tick = tick
        return self

    def right(self, *, axis: AxisOptions | None = None, tick: TickOptions | None) -> Self:
        self.right_axis = axis
        self.right_tick = tick
        return self
