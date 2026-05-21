from typing import Literal

from pydantic import Field

from athena_charts.themes._base import FontWeight
from athena_charts_matplotlib.options.base import BaseOptions

type FontFamily = Literal["sans-serif", "serif", "monospace", "cursive", "fantasy"]


class MatplotlibFontOptions(BaseOptions):
    family: FontFamily | None = Field(None, description="默认字体族")
    fonts: list[str] | None = Field(None, description="字体列表")
    color: str | None = Field(None, description="默认文本颜色")
    weight: FontWeight | None = Field(None, description="字体粗细")
