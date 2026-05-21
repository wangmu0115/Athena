from pydantic import BaseModel, ConfigDict, Field

from athena_charts.specs.plots.types import MarkerShape
from athena_charts.themes import FontWeight


class _BaseStyle(BaseModel):
    # 禁止未知字段, 允许自定义对象, 自动 trim
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, str_strip_whitespace=True)


class ResolvedDataLabelStyle(_BaseStyle):
    color: str | None = Field(None, description="颜色")
    fontsize: int | None = Field(None, gt=0, description="字号")
    fontweight: FontWeight | None = Field(None, description="字体粗细")


class ResolvedMarkerStyle(_BaseStyle):
    shape: MarkerShape | None = Field(None, description="标记形状")
    size: float | None = Field(None, gt=0, description="标记大小")
    color: str | None = Field(None, description="标记填充颜色")
    edge_color: str | None = Field(None, description="标记边框颜色")
    edge_width: float | None = Field(None, ge=0, description="标记边框宽度")
    alpha: float | None = Field(None, ge=0, le=1, description="标记透明度")
    z_index: int | None = Field(None, description="标记绘制层级")
