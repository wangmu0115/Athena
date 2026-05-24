from typing import Self

from pydantic import Field, model_validator

from athena_charts.specs._base import _BaseSpec
from athena_charts.specs.coords.tick import TickSpec
from athena_charts.specs.coords.types import AxisDataType, AxisScale


class AxisSpec(_BaseSpec):
    label: str = Field("", description="坐标轴标题")
    data_type: AxisDataType = Field("number", description="坐标轴数据类型")
    scale: AxisScale = Field("linear", description="坐标轴缩放方式。")
    domain_min: object | None = Field(None, description="坐标轴数据域最小值，类型应与坐标轴数据类型兼容。")
    domain_max: object | None = Field(None, description="坐标轴数据域最大值，类型应与坐标轴数据类型兼容。")
    tick: TickSpec = Field(default_factory=TickSpec, description="坐标轴配置项")

    @model_validator(mode="after")
    def validate(self) -> Self:
        if self.options.scale == "log" and self.data_type != "number":
            raise ValueError("Only number axis can use log scale.")
        return self
