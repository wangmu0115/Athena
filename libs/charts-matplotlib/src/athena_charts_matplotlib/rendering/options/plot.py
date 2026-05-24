from pydantic import Field

from athena_charts.specs.rules.conditions import DataCondition
from athena_charts_matplotlib.adapters.styles import to_mpl_line_style
from athena_charts_matplotlib.rendering.options.base import _BaseOptions
from athena_charts_matplotlib.styles.types import FontWeight, LineStyle, MarkerShape


class OptionsRule(_BaseOptions):
    """条件样式规则基类。"""

    when: DataCondition = Field(..., description="规则生效条件")


class LineOptions(_BaseOptions):
    linewidth: float | None = Field(None, gt=0, description="线宽")
    linestyle: LineStyle | None = Field(None, description="线型")
    linecolor: str | None = Field(None, description="线的颜色", alias="color")


class MarkerOptions(_BaseOptions):
    visible: bool = Field(False, description="是否显示数据点标记")
    shape: MarkerShape | None = Field(None, description="标记形状", alias="marker")
    size: float | None = Field(None, gt=0, description="标记大小", alias="markersize")
    facecolor: str | None = Field(None, description="标记填充颜色", alias="markerfacecolor")
    edgecolor: str | None = Field(None, description="标记边框颜色", alias="markeredgecolor")
    edgewidth: float | None = Field(None, ge=0, description="标记边框宽度", alias="markeredgewidth")


class DataLabelOptions(_BaseOptions):
    visible: bool = Field(False, description="是否显示数据标签")
    formatter: str | None = Field(
        None,
        description="标签格式模板，例如 `{y:+g}`、`({x}, {y})`、`{name}: {percent:.1%}`",
    )
    color: str | None = Field(None, description="默认颜色")
    fontsize: int | None = Field(None, gt=0, description="字号")
    fontweight: FontWeight | None = Field(None, description="字体粗细")


class LinePlotOptions(_BaseOptions):
    line: LineOptions
    marker: MarkerOptions
    data_label: DataLabelOptions

    def build_plot_params(self) -> dict[str, object]:
        params: dict[str, object] = {}
        if self.line is not None:
            params.update(self.line.model_dump(exclude_none=True, by_alias=True, exclude=["linestyle"]))
            if self.line.linestyle is not None:
                params["linestyle"] = to_mpl_line_style(self.line.linestyle)
        if self.marker is not None:
            if self.marker.visible:
                params.update(self.marker.model_dump(exclude_none=True, by_alias=True, exclude=["visible"]))
            else:
                params["marker"] = None
        return params
