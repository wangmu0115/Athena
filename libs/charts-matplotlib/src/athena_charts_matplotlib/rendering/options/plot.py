from pydantic import Field

from athena_charts.specs.rules.conditions import DataCondition
from athena_charts_matplotlib.rendering.options.base import _BaseOptions
from athena_charts_matplotlib.styles.types import LineStyle


class OptionsRule(_BaseOptions):
    """条件样式规则基类。"""

    when: DataCondition = Field(..., description="规则生效条件")


class LineOptions(_BaseOptions):
    linewidth: float | None = Field(None, gt=0, description="线宽")
    linestyle: LineStyle | None = Field(None, description="线型")
    linecolor: str | None = Field(None, description="线的颜色")


class MarkerOptions(_BaseOptions):
    visible: bool = Field(False, description="是否显示数据点标记")

    shape: MarkerShape | None = Field(None, description="标记形状")
    size: float | None = Field(None, gt=0, description="标记大小")
    color: str | None = Field(None, description="标记填充颜色")
    edge_color: str | None = Field(None, description="标记边框颜色")
    edge_width: float | None = Field(None, ge=0, description="标记边框宽度")
    alpha: float | None = Field(None, ge=0, le=1, description="标记透明度")
    z_index: int | None = Field(None, description="标记绘制层级")
