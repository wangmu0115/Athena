from typing import Literal, Self

from pydantic import Field, model_validator

from athena_core.models import BaseAthenaModel


class TickFormatter(BaseAthenaModel):
    kind: Literal[
        "auto",
        "number",
        "category",
        "datetime",
        "date",
        "time",
        "percent",
        "currency",
    ] = Field("auto", description="格式化类型，auto 表示由引擎根据轴数据类型自动推断")
    precision: int | None = Field(None, ge=0, description="数值精度")
    prefix: str = Field("", description="前缀")
    suffix: str = Field("", description="后缀")
    datetime_format: str | None = Field(None, description="日期时间格式")


class TickOptions(BaseAthenaModel):
    visible: bool = Field(True, description="是否显示刻度")
    label_visible: bool = Field(True, description="是否显示刻度标签")
    label_rotation: float = Field(0.0, description="刻度标签旋转角度")
    formatter: TickFormatter = Field(default_factory=TickFormatter, description="刻度格式化配置")
    strategy: Literal[
        "auto",
        "all",
        "sample",
        "fixed",
        "none",
    ] = Field("auto", description="刻度选择策略")
    max_count: int | None = Field(None, gt=0, description="sample/auto 策略下最多显示的刻度数量")
    fixed_values: list[object] | None = Field(None, description="fixed 策略下固定展示的刻度值")

    @model_validator(mode="after")
    def validate_fixed_ticks(self) -> Self:
        if self.strategy == "fixed" and not self.fixed_values:
            raise ValueError("TickOptions.fixed_values is required when strategy='fixed'.")
        return self


class AxisSpec(BaseAthenaModel):
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

    @model_validator(mode="after")
    def validate_scale_and_range(self) -> Self:
        if self.scale == "log" and self.data_type != "number":
            raise ValueError("Only number axis can use log scale.")

        if self.min_value is not None and self.max_value is not None and self.min_value >= self.max_value:
            raise ValueError("Axis.min_value must be less than Axis.max_value.")

        return self


class CartesianAxis(AxisSpec):
    """笛卡尔坐标轴，X 轴通常是 bottom/top，Y 轴通常是 left/right"""

    position: Literal[
        "bottom",
        "top",
        "left",
        "right",
    ] = Field(..., description="坐标轴位置")

    @model_validator(mode="after")
    def validate_cartesian_axis(self) -> Self:
        if self.position in {"left", "right"} and self.data_type != "number":
            raise ValueError("Cartesian Y axis must be number data_type.")
        return self


class PolarAxis(AxisSpec):
    """极坐标轴：角度轴 (theta) 和半径轴 (radius)"""

    role: Literal["theta", "radius"] = Field(..., description="极坐标轴角色")
