from typing import Self

from pydantic import Field, model_validator

from athena_charts.specs._base import _BaseOptions
from athena_charts.specs.coords.types import TickLabelFormatKind, TickLocatorStrategy


class TickLabelFormat(_BaseOptions):
    kind: TickLabelFormatKind = Field("auto", description="刻度标签格式化类型")
    precision: int | None = Field(None, ge=0, description="数值精度")
    prefix: str = Field("", description="前缀")
    suffix: str = Field("", description="后缀")
    time_format: str | None = Field(None, description="时间字符串输出格式")
    date_format: str | None = Field(None, description="日期字符串输出格式")
    datetime_format: str | None = Field(None, description="日期时间字符串输出格式")


class TickLocator(_BaseOptions):
    strategy: TickLocatorStrategy = Field("auto", description="刻度位置选择策略")
    max_count: int | None = Field(None, gt=0, description="自动策略下最多生成或展示的刻度数量")
    fixed_values: list[object] | None = Field(None, description="fixed 策略下使用的固定刻度值")

    @model_validator(mode="after")
    def validate(self) -> Self:
        if self.strategy == "fixed" and not self.fixed_values:
            raise ValueError("TickLocator.fixed_values is required when strategy='fixed'.")
        return self


class TickOptions(_BaseOptions):
    visible: bool | None = Field(None, description="是否显示刻度")
    label_visible: bool | None = Field(None, description="是否显示刻度标签")
    label_rotation: float | None = Field(0.0, ge=-90, le=90, description="刻度标签旋转角度")
    label_format: TickLabelFormat = Field(default_factory=TickLabelFormat, description="刻度格式化配置")
    locator: TickLocator = Field(default_factory=TickLocator, description="刻度位置配置")
