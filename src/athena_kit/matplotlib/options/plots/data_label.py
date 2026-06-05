from typing import Self

from pydantic import Field

from athena_kit.matplotlib.options._base import _BaseOptions
from athena_kit.matplotlib.options.rules import DataCondition
from athena_kit.matplotlib.types import FontWeight, HorizontalAlignment, VerticalAlignment


class DataLabelStyle(_BaseOptions):
    visible: bool = Field(False, description="是否显示数据标签")
    formatter: str | None = Field(
        None,
        description="标签格式模板，例如 `{y:+g}`、`({x}, {y})`、`{name}: {percent:.1%}`",
    )
    color: str | None = Field(None, description="默认颜色")
    fontsize: int | None = Field(None, gt=0, description="字号")
    fontweight: FontWeight | None = Field(None, description="字体粗细")

    @classmethod
    def hide(cls) -> Self:
        return cls(visible=False)

    @classmethod
    def show(
        cls,
        formatter: str | None = None,
        *,
        color: str | None = None,
        fontsize: int | None = None,
        fontweight: FontWeight | None = None,
    ):
        return cls(
            visible=True,
            formatter=formatter,
            color=color,
            fontsize=fontsize,
            fontweight=fontweight,
        )


class DataLabelStyleRule(_BaseOptions):
    when: DataCondition = Field(..., description="生效条件")
    style: DataLabelStyle = Field(..., description="满足条件时应用的标记点样式")


class DataLabelOptions(DataLabelStyle):
    offset_x: float = Field(0, description="标签 X 方向偏移量，单位为 points")
    offset_y: float = Field(6, description="标签 Y 方向偏移量，单位为 points")
    ha: HorizontalAlignment = Field("center", description="水平对齐方式")
    va: VerticalAlignment = Field("bottom", description="垂直对齐方式")

    rules: list[DataLabelStyleRule] = Field(default_factory=list, description="条件样式规则")

    @classmethod
    def show(
        cls,
        formatter: str | None = None,
        *,
        color: str | None = None,
        fontsize: int | None = None,
        fontweight: FontWeight | None = None,
        offset_x: float = 0,
        offset_y: float = 6,
        ha: HorizontalAlignment = "center",
        va: VerticalAlignment = "bottom",
    ):
        return cls(
            visible=True,
            formatter=formatter,
            color=color,
            fontsize=fontsize,
            fontweight=fontweight,
            offset_x=offset_x,
            offset_y=offset_y,
            ha=ha,
            va=va,
        )

    def add_rule(self, when: DataCondition, style: DataLabelStyle) -> Self:
        self.rules.append(DataLabelStyleRule(when=when, style=style))
        return self

    def style_model_dump(self, by_alias=False) -> dict[str, object]:
        return self.model_dump(
            exclude_none=True,
            include=["visible", "formatter", "color", "fontsize", "fontweight"],
            by_alias=by_alias,
        )
