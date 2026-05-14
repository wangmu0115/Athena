import math
from typing import Self

from pydantic import Field

from athena_charts.charts import Chart
from athena_core.models.base import BaseAthenaModel


class FigureGridLayout(BaseAthenaModel):
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
            raise ValueError("chart_count must be greater than 0.")
        if chart_count == 1:
            return cls(rows=1, cols=1)

        cols = math.ceil(math.sqrt(chart_count))
        rows = math.ceil(chart_count / cols)
        return cls(rows=rows, cols=cols)


class ChartPlacement(BaseAthenaModel):
    chart: Chart = Field(..., description="需要放置的图表")
    row: int | None = Field(None, gt=0, description="所在行号，从 1 开始")
    col: int | None = Field(None, gt=0, description="所在列号，从 1 开始")
    row_span: int = Field(1, gt=0, description="跨越的行数")
    col_span: int = Field(1, gt=0, description="跨越的列数")
