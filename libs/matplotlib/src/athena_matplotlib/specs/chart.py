from typing import Self

from pydantic import Field, model_validator

from athena_charts.specs.plots import PlotSpec
from athena_charts.specs.types import BarLayoutMode
from athena_matplotlib.options.chart import ChartOptions
from athena_matplotlib.specs._base import _BaseSpec
from athena_matplotlib.specs.coords import CoordSpec


class ChartSpec(_BaseSpec):
    title: str = Field("", description="图表标题")
    coord: CoordSpec = Field(..., description="坐标系统")
    plots: list[PlotSpec] = Field(default_factory=list, description="图层列表")

    chart_options: ChartOptions | None = Field(None, description="图表运行时配置")

    bar_layout: BarLayoutMode = Field("group", description="当具有多个 Bar 图层时的布局方式")
    category_order: list[object] | None = Field(None, description="多个图层 X 轴对齐时的特定顺序")

    @model_validator(mode="after")
    def validate_coord_plots(self) -> Self:
        for plot in self.plots:
            plot.validate_coord(self.coord)  # 校验坐标系
        return self
