from pydantic import Field

from athena_charts.specs._base import _BaseOptions
from athena_charts.specs.rules import DataLabelStyleRule
from athena_charts.themes import FontWeight


class DataLabelOptions(_BaseOptions):
    visible: bool = Field(False, description="是否显示数据标签")
    formatter: str | None = Field(
        None,
        description="标签格式模板，例如 `{y:+g}`、`({x}, {y})`、`{name}: {percent:.1%}`",
    )
    clip_on: bool = Field(True, description="是否裁剪到绘图区内")

    color: str | None = Field(None, description="默认颜色")
    fontsize: int | None = Field(None, gt=0, description="字号")
    fontweight: FontWeight | None = Field(None, description="字体粗细")

    style_rules: list[DataLabelStyleRule] = Field(default_factory=list, description="动态样式，命中多个规则时按顺序合并")
