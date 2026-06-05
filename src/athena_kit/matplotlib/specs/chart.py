from typing import Self

from pydantic import Field, model_validator

from athena_kit.matplotlib.options.chart import ChartOptions
from athena_kit.matplotlib.specs._base import _BaseSpec
from athena_kit.matplotlib.specs.coords import CoordSpec
from athena_kit.matplotlib.specs.plots import PlotSpec
from athena_kit.matplotlib.types import BarLayoutMode


class ChartSpec(_BaseSpec):
    title: str | None = Field(None, description="图表标题")
    coord: CoordSpec = Field(..., description="坐标系统")
    plots: list[PlotSpec] = Field(default_factory=list, description="图层列表")
    bar_layout_mode: BarLayoutMode = Field("group", description="当具有多个 Bar 图层时的布局方式")
    category_order: list[object] | None = Field(None, description="多个图层 X 轴对齐时的特定顺序")

    options: ChartOptions | None = Field(None, description="图表运行时样式配置")

    @model_validator(mode="after")
    def validate_coord_plots(self) -> Self:
        for plot in self.plots:
            plot.validate_coord(self.coord)  # 校验坐标系
        return self

    @classmethod
    def of(
        cls,
        coord: CoordSpec,
        *,
        plots: list[PlotSpec] | None = None,
        bar_layout_mode: BarLayoutMode = "group",
        category_order: list[object] | None = None,
        title: str | None = None,
        options: ChartOptions | None = None,
    ) -> Self:
        return cls(
            title=title,
            coord=coord,
            plots=plots or [],
            bar_layout_mode=bar_layout_mode,
            category_order=category_order,
            options=options,
        )

    def add_plot(self, plot: PlotSpec) -> Self:
        plot.validate_coord(self.coord)  # validate
        self.plots.append(plot)

        return self
