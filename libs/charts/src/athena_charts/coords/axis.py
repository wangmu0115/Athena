from typing import Literal

from pydantic import Field

from athena_core.models import BaseAthenaModel


class TickFormatter(BaseAthenaModel):
    kind: Literal[
        "number",
        "category",
        "datetime",
        "date",
        "time",
        "percent",
        "currency",
    ] = Field("number", description="格式化类型")
    precision: int | None = Field(None, ge=0, description="数值精度")
    prefix: str = Field("", description="前缀")
    suffix: str = Field("", description="后缀")
    datetime_format: str | None = Field(None, description="日期时间格式")


class TickOptions(BaseAthenaModel):
    visible: bool = Field(True, description="是否显示刻度")
    label_visible: bool = Field(True, description="是否显示刻度标签")
    label_rotation: float = Field(0.0, description="刻度标签旋转角度")
    formatter: TickFormatter = Field(default_factory=TickFormatter, description="刻度格式化配置")


class BaseAxis(BaseAthenaModel):
    label: str = Field("", description="坐标轴标题")
    visible: bool = Field(True, description="是否显示坐标轴")
    data_type: Literal[
        "timestamp_ms",
        "timestamp_s",
        "datetime",
        "date",
        "time",
        "number",
        "category",
    ] = Field("number", description="坐标轴数据类型")
    scale: Literal["linear", "log"] = Field("linear", description="坐标轴缩放方式")
    min_value: float | None = Field(None, description="最小值")
    max_value: float | None = Field(None, description="最大值")
    ticks: TickOptions = Field(default_factory=TickOptions, description="刻度配置")


class CartesianAxis(BaseAxis):
    """笛卡尔坐标轴，X 轴通常是 bottom/top，Y 轴通常是 left/right"""

    position: Literal[
        "bottom",
        "top",
        "left",
        "right",
    ] = Field(..., description="坐标轴位置")


class PolarAxis(BaseAxis):
    """极坐标轴：角度轴 (theta) 和半径轴 (radius)"""

    role: Literal["theta", "radius"] = Field(..., description="极坐标轴角色")
