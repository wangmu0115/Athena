from typing import Self

from pydantic import Field, model_validator

from athena_charts.specs._base import _BaseSpec
from athena_charts.specs.coords import CoordSpec
from athena_charts.specs.plots import PlotSpec
from athena_charts.specs.types import BarLayoutMode


class ChartLabels(_BaseSpec):
    title: str = Field("", description="图表标题")
    subtitle: str = Field("", description="图表副标题")


class ChartSpec(_BaseSpec):
    labels: ChartLabels = Field(default_factory=ChartLabels, description="图表文本标签")
    coord: CoordSpec = Field(..., description="坐标系统")
    plots: list[PlotSpec] = Field(default_factory=list, description="图层列表")

    bar_layout: BarLayoutMode = Field("group", description="当具有多个 Bar 图层时的布局方式")
    category_order: list[object] | None = Field(None, description="多个图层 X 轴对齐时的特定顺序")

    @model_validator(mode="after")
    def validate_coord_and_plots(self) -> Self:
        if not self.plots:
            raise ValueError("Chart must contain at least one plot.")

        for plot in self.plots:
            plot.validate_coord(self.coord)  # 校验坐标系

        return self
