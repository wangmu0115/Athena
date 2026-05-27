from typing import Self

from pydantic import Field

from athena_matplotlib.specs._base import _BaseSpec
from athena_matplotlib.types import TickLabelFormatKind, TickLocatorStrategy


class TickLabelFormatter(_BaseSpec):
    kind: TickLabelFormatKind = Field("auto", description="刻度标签格式化类型")
    precision: int | None = Field(None, ge=0, description="数值精度")
    prefix: str = Field("", description="前缀")
    suffix: str = Field("", description="后缀")
    time_format: str | None = Field(None, description="时间字符串输出格式")
    date_format: str | None = Field(None, description="日期字符串输出格式")
    datetime_format: str | None = Field(None, description="日期时间字符串输出格式")

    @classmethod
    def auto(cls) -> Self:
        return cls(kind="auto")

    @classmethod
    def number(cls, precision: int | None = 2, prefix: str = "", suffix: str = "") -> Self:
        return cls(kind="number", precision=precision, prefix=prefix, suffix=suffix)

    @classmethod
    def currency(cls, *, precision: int | None = 2, prefix: str = "¥", suffix: str = "Yuan") -> Self:
        return cls(kind="currency", precision=precision, prefix=prefix, suffix=suffix)

    @classmethod
    def percent(cls, *, precision: int | None = 2, suffix: str = "%") -> Self:
        return cls(kind="percent", precision=precision, suffix=suffix)

    @classmethod
    def datetime(cls, *, datetime_format: str = "%Y-%m-%d %H:%M:%S") -> Self:
        return cls(kind="datetime", datetime_format=datetime_format)

    @classmethod
    def date(cls, *, date_format: str = "%Y-%m-%d") -> Self:
        return cls(kind="date", date_format=date_format)

    @classmethod
    def time(cls, *, time_format: str = "%H:%M:%S") -> Self:
        return cls(kind="time", time_format=time_format)

    @classmethod
    def timestamp(cls, *, precision: int | None = 2, unit: str = "ms") -> Self:
        return cls(kind="number", precision=precision, suffix=unit)


class TickLocator(_BaseSpec):
    strategy: TickLocatorStrategy = Field("auto", description="刻度位置选择策略")
    max_count: int | None = Field(None, gt=0, description="自动策略下最多生成或展示的刻度数量")
    fixed_values: list[object] | None = Field(None, description="fixed 策略下使用的固定刻度值")

    @classmethod
    def auto(cls, max_count: int = 6) -> Self:
        return cls(strategy="auto", max_count=max_count)

    @classmethod
    def fixed(cls, fixed_values: list[object]) -> Self:
        return cls(strategy="fixed", fixed_values=fixed_values)

    @classmethod
    def all(cls) -> Self:
        return cls(strategy="all")

    @classmethod
    def none(cls) -> Self:
        return cls(strategy="none")


class TickSpec(_BaseSpec):
    formatter: TickLabelFormatter = Field(..., description="刻度格式化配置")
    locator: TickLocator = Field(..., description="刻度位置配置")

    @classmethod
    def of(
        cls,
        formatter: TickLabelFormatter | None = None,
        locator: TickLocator | None = None,
    ) -> Self:
        return cls(
            formatter=formatter or TickLabelFormatter.auto(),
            locator=locator or TickLocator.auto(max_count=6),
        )
