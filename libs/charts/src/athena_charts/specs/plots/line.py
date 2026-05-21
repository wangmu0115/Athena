from typing import Literal, Self

from pydantic import Field

from athena_charts.specs._base import _BaseOptions, _BaseSpec
from athena_charts.specs.coords import Coord
from athena_charts.specs.plots.base import Plot
from athena_charts.specs.plots.datas import XYSeriesData
from athena_charts.specs.plots.options.labels import DataLabelOptions
from athena_charts.specs.plots.options.markers import MarkerOptions
from athena_charts.specs.plots.types import LineStyle


class LinePlotData(_BaseSpec):
    data: XYSeriesData = Field(..., description="折线图数据")


class LinePlotOptions(_BaseOptions):
    opacity: float | None = Field(None, ge=0, le=1, description="透明度")
    x_axis_side: Literal["bottom", "top"] = Field("bottom", description="使用主 X 轴(bottom)或辅助 X 轴(top)")
    y_axis_side: Literal["left", "right"] = Field("left", description="使用左侧或右侧 Y 轴")
    line_width: float | None = Field(None, gt=0, description="折线宽度")
    line_style: LineStyle | None = Field(None, description="线型")

    data_label: DataLabelOptions = Field(default_factory=DataLabelOptions, description="值标签配置")
    marker: MarkerOptions = Field(default_factory=MarkerOptions, description="数据点标记配置")


class LinePlot(Plot):
    kind: Literal["line"] = Field("line", description="折线图")
    coord_kind: Literal["cartesian"] = Field("cartesian", description="笛卡尔坐标系")
    data: LinePlotData = Field(..., description="图层数据")
    options: LinePlotOptions = Field(default_factory=LinePlotOptions, description="折线图配置")

    @classmethod
    def build(cls, *, data: XYSeriesData, options: LinePlotOptions) -> Self:
        return cls(
            data=LinePlotData(data=data),
            options=options,
        )

    def validate_coord(self, coord: Coord):
        super().validate_coord(coord)
        if self.options.x_axis_side == "bottom" and coord.x_axis is None:
            raise ValueError()

        if coord.get_y_axis(self.options.y_axis_side) is None:
            raise ValueError(f"Plot {self.name or self.kind} uses {self.options.y_axis_side} Y axis, but coord does not define it.")
