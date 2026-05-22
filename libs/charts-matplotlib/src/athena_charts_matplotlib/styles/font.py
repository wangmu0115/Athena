from pydantic import Field

from athena_charts.themes import FontWeight
from athena_charts_matplotlib.styles._base import _BaseStyle
from athena_charts_matplotlib.styles.types import FontFamily


class MatplotlibFontStyle(_BaseStyle):
    family: FontFamily | None = Field(None, description="默认字体族")
    fallbacks: list[str] | None = Field(None, description="字体列表")
    size: int | None = Field(None, gt=0, description="字号")
    weight: FontWeight | None = Field(None, description="字体粗细")
    color: str | None = Field(None, description="默认文本颜色")
