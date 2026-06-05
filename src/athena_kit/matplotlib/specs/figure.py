from typing import Self

from pydantic import Field

from athena_kit.matplotlib.specs._base import _BaseSpec
from athena_kit.matplotlib.specs.chart import ChartSpec


class ChartPlacement(_BaseSpec):
    """Chart 在 Figure 网格中的放置位置"""

    chart: ChartSpec = Field(..., description="需要放置的图表")
    row: int = Field(1, gt=0, description="所在行号，从 1 开始")
    col: int = Field(1, gt=0, description="所在列号，从 1 开始")
    row_span: int = Field(1, gt=0, description="跨越的行数")
    col_span: int = Field(1, gt=0, description="跨越的列数")

    @classmethod
    def of(
        cls,
        chart: ChartSpec,
        row: int = 1,
        col: int = 1,
        *,
        row_span: int = 1,
        col_span: int = 1,
    ) -> Self:
        return cls(
            chart=chart,
            row=row,
            col=col,
            row_span=row_span,
            col_span=col_span,
        )


class FigureGridLayout(_BaseSpec):
    rows: int = Field(1, gt=0, description="图表网格行数")
    cols: int = Field(1, gt=0, description="图表网格列数")
    share_x: bool = Field(False, description="是否共享 X 轴")
    share_y: bool = Field(False, description="是否共享 Y 轴")
    hspace: float | None = Field(None, ge=0, description="图表行间距")
    wspace: float | None = Field(None, ge=0, description="图表列间距")

    @classmethod
    def of(
        cls,
        rows: int = 1,
        cols: int = 1,
        *,
        share_x: bool = False,
        share_y: bool = False,
        hspace: float | None = None,
        wspace: float | None = None,
    ) -> Self:
        return cls(
            rows=rows,
            cols=cols,
            share_x=share_x,
            share_y=share_y,
            hspace=hspace,
            wspace=wspace,
        )


class FigureSpec(_BaseSpec):
    """画布语义模型，Figure 是顶层容器，负责组织一个或多个 Chart"""

    title: str | None = Field(None, description="画布标题")
    layout: FigureGridLayout = Field(..., description="图表网格布局")
    charts: list[ChartPlacement] = Field(default_factory=list, description="画布中的图表放置列表")

    @classmethod
    def from_chart(cls, chart: ChartSpec, *, title: str | None = None) -> Self:
        return cls.of(
            FigureGridLayout.of(1, 1),
            title=title,
        ).add_chart(chart)

    @classmethod
    def of(
        cls,
        layout: FigureGridLayout,
        *,
        charts: list[ChartPlacement] | None = None,
        title: str | None = None,
    ) -> Self:
        return cls(
            layout=layout,
            charts=charts or [],
            title=title,
        )

    def add_chart(
        self,
        chart: ChartSpec,
        row: int = 1,
        col: int = 1,
        *,
        row_span: int = 1,
        col_span: int = 1,
    ) -> Self:
        self.charts.append(ChartPlacement.of(chart, row, col, row_span=row_span, col_span=col_span))
        return self
