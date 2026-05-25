import math
from typing import Self

from pydantic import Field, model_validator

from athena_charts.specs._base import _BaseSpec
from athena_charts.specs.charts import ChartSpec


class ChartPlacement(_BaseSpec):
    """Chart 在 Figure 网格中的放置位置"""

    chart: ChartSpec = Field(..., description="需要放置的图表")
    row: int | None = Field(None, gt=0, description="所在行号，从 1 开始")
    col: int | None = Field(None, gt=0, description="所在列号，从 1 开始")
    row_span: int = Field(1, gt=0, description="跨越的行数")
    col_span: int = Field(1, gt=0, description="跨越的列数")


class FigureLabels(_BaseSpec):
    title: str = Field("", description="画布标题")
    subtitle: str = Field("", description="画布副标题")


class FigureGridLayout(_BaseSpec):
    rows: int | None = Field(None, gt=0, description="图表网格行数")
    cols: int | None = Field(None, gt=0, description="图表网格列数")
    share_x: bool = Field(False, description="是否共享 X 轴")
    share_y: bool = Field(False, description="是否共享 Y 轴")
    hspace: float | None = Field(None, ge=0, description="图表行间距")
    wspace: float | None = Field(None, ge=0, description="图表列间距")

    @classmethod
    def from_chart_count(cls, chart_count: int) -> Self:
        """根据图表数量推断接近正方形的网格布局"""
        if chart_count <= 0:
            raise ValueError("Chart count must be greater than 0.")
        if chart_count == 1:
            return cls(rows=1, cols=1)

        cols = math.ceil(math.sqrt(chart_count))
        rows = math.ceil(chart_count / cols)
        return cls(rows=rows, cols=cols)


class FigureSpec(_BaseSpec):
    """画布语义模型，Figure 是顶层容器，负责组织一个或多个 Chart"""

    labels: FigureLabels = Field(default_factory=FigureLabels, description="画布级文本标签")
    layout: FigureGridLayout | None = Field(None, description="图表网格布局")
    charts: list[ChartPlacement] = Field(default_factory=list, description="画布中的图表放置列表")

    @classmethod
    def from_chart(cls, chart: ChartSpec) -> Self:
        return cls(
            layout=FigureGridLayout.from_chart_count(1),
            charts=[ChartPlacement(chart=chart, row=1, col=1)],
        )

    @classmethod
    def from_charts(cls, charts: list[ChartSpec]) -> Self:
        return cls(
            charts=[ChartPlacement(chart=chart) for chart in charts],
        )

    @model_validator(mode="after")
    def validate_and_resolve_layout(self) -> Self:
        # if not self.charts:
        #     raise ValueError("Figure must contain at least one chart.")

        # if self.layout is None:
        #     self.layout = FigureGridLayout.from_chart_count(len(self.charts))
        # rows = self.layout.rows
        # cols = self.layout.cols
        # if rows is None or cols is None:
        #     raise ValueError("Figure layout rows and cols cannot both be empty.")

        # resolved_charts: list[ChartPlacement] = []
        # for index, placement in enumerate(self.charts):
        #     row = placement.row if placement.row is not None else index // cols + 1
        #     col = placement.col if placement.col is not None else index % cols + 1
        #     if row + placement.row_span - 1 > rows:
        #         raise ValueError("Chart placement row span exceeds figure layout rows.")
        #     if col + placement.col_span - 1 > cols:
        #         raise ValueError("Chart placement col span exceeds figure layout cols.")

        #     resolved_charts.append(placement.model_copy(update={"row": row, "col": col}))

        # self.charts = resolved_charts
        return self
