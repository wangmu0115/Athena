from pydantic import Field

from athena_charts.themes._base import _BaseTheme
from athena_charts.themes.types import FontWeight


class FontTheme(_BaseTheme):
    family: str | None = Field(None, description="默认字体族")
    fallbacks: list[str] | None = Field(None, description="字体回退列表")
    color: str | None = Field(None, description="默认文本颜色")
    weight: FontWeight | None = Field(None, description="字体粗细")
