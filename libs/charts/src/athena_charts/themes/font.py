from pydantic import Field

from athena_charts.themes.base import BaseTheme, FontWeight


class FontTheme(BaseTheme):
    family: str | None = Field(None, description="默认字体族")
    fallbacks: list[str] | None = Field(None, description="字体回退列表")
    color: str | None = Field(None, description="默认文本颜色")
    wight: FontWeight | None = Field(None, description="字体粗细")
