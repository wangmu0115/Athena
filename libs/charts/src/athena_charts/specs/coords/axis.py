from typing import Self

from pydantic import Field, model_validator

from athena_charts.specs._base import _BaseOptions, _BaseSpec
from athena_charts.specs.coords.ticks import TickOptions
from athena_charts.specs.coords.types import AxisDataType, AxisScale


class AxisOptions(_BaseOptions):
    visible: bool | None = Field(None, description="是否显示坐标轴")
    scale: AxisScale = Field("linear", description="坐标轴缩放方式。")
    domain_min: object | None = Field(None, description="坐标轴数据域最小值，类型应与坐标轴数据类型兼容。")
    domain_max: object | None = Field(None, description="坐标轴数据域最大值，类型应与坐标轴数据类型兼容。")
    ticks: TickOptions = Field(default_factory=TickOptions, description="刻度配置")

    @model_validator(mode="after")
    def validate(self) -> Self:
        if self.domain_min is not None and self.domain_max is not None and self.domain_min > self.domain_max:
            raise ValueError("Axis domain_max must be greater than domain_min.")
        return self


class AxisSpec(_BaseSpec):
    label: str = Field("", description="坐标轴标题")
    data_type: AxisDataType = Field("number", description="坐标轴数据类型")
    options: AxisOptions = Field(default_factory=AxisOptions, description="坐标轴配置项")

    @model_validator(mode="after")
    def validate(self) -> Self:
        if self.options.scale == "log" and self.data_type != "number":
            raise ValueError("Only number axis can use log scale.")
        return self
