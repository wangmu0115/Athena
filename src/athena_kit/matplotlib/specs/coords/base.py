from typing import Self

from pydantic import Field, model_validator

from athena_kit.matplotlib.specs._base import _BaseSpec
from athena_kit.matplotlib.specs.coords.tick import TickSpec
from athena_kit.matplotlib.types import AxisDataType, CoordKind
from athena_kit.matplotlib.types.styles import AxisScale


class AxisSpec(_BaseSpec):
    label: str | None = Field(None, description="坐标轴标题")
    data_type: AxisDataType = Field("number", description="坐标轴数据类型")
    scale: AxisScale = Field("linear", description="坐标轴缩放方式")
    min: object | None = Field(None, description="坐标轴数据域最小值，类型应与坐标轴数据类型兼容")
    max: object | None = Field(None, description="坐标轴数据域最大值，类型应与坐标轴数据类型兼容")
    tick: TickSpec | None = Field(None, description="坐标轴配置项")

    @model_validator(mode="after")
    def validate(self) -> Self:
        if self.scale == "log" and self.data_type != "number":
            raise ValueError("Only number axis can use log scale.")
        return self


class Coord(_BaseSpec):
    kind: CoordKind = Field(..., description="坐标系统类型")
