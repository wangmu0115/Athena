from typing import Self

from pydantic import Field

from athena_kit.matplotlib.options._base import _BaseOptions
from athena_kit.matplotlib.options.rules import DataCondition
from athena_kit.matplotlib.types import MarkerShape


class MarkerStyle(_BaseOptions):
    marker: MarkerShape | None = Field(None, description="标记形状")
    markersize: float | None = Field(None, gt=0, description="标记大小")
    marker_facecolor: str | None = Field(None, description="标记填充颜色", alias="markerfacecolor")
    marker_edgecolor: str | None = Field(None, description="标记边框颜色", alias="markeredgecolor")
    marker_edgewidth: float | None = Field(None, ge=0, description="标记边框宽度", alias="markeredgewidth")

    @classmethod
    def hide(cls) -> Self:
        return cls(marker=None)

    @classmethod
    def show(
        cls,
        marker: MarkerShape = "circle",
        *,
        markersize: float | None = None,
        marker_facecolor: str | None = None,
        marker_edgecolor: str | None = None,
        marker_edgewidth: float | None = None,
    ):
        return cls(
            marker=marker,
            markersize=markersize,
            marker_facecolor=marker_facecolor,
            marker_edgecolor=marker_edgecolor,
            marker_edgewidth=marker_edgewidth,
        )


class MarkerStyleRule(_BaseOptions):
    when: DataCondition = Field(..., description="生效条件")
    style: MarkerStyle = Field(..., description="满足条件时应用的标记点样式")


class MarkerOptions(MarkerStyle):
    rules: list[MarkerStyleRule] = Field(default_factory=list, description="条件样式规则")

    def add_rule(self, when: DataCondition, style: MarkerStyle) -> Self:
        self.rules.append(MarkerStyleRule(when=when, style=style))
        return self
