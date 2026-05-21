from pydantic import Field

from athena_charts.specs._base import _BaseOptions
from athena_charts.specs.plots.types import MarkerShape
from athena_charts.specs.rules import MarkerStyleRule


class MarkerOptions(_BaseOptions):
    visible: bool = Field(False, description="是否显示数据点标记")

    shape: MarkerShape | None = Field(None, description="标记形状")
    size: float | None = Field(None, gt=0, description="标记大小")
    color: str | None = Field(None, description="标记填充颜色")
    edge_color: str | None = Field(None, description="标记边框颜色")
    edge_width: float | None = Field(None, ge=0, description="标记边框宽度")
    alpha: float | None = Field(None, ge=0, le=1, description="标记透明度")
    z_index: int | None = Field(None, description="标记绘制层级")

    style_rules: list[MarkerStyleRule] = Field(default_factory=list, description="动态样式规则")
