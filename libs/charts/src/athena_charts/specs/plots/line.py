from typing import Literal

from pydantic import Field

from athena_charts.specs.plots.base import Plot
from athena_charts.specs.plots.data import LinePlotData
from athena_charts.specs.plots.options import LinePlotOptions


class LinePlot(Plot):
    kind: Literal["line"] = Field("line", description="折线图")
    coord_kind: Literal["cartesian"] = Field("cartesian", description="笛卡尔坐标系")
    data: LinePlotData = Field(..., description="图层数据")
    options: LinePlotOptions = Field(default_factory=LinePlotOptions, description="折线图配置")
