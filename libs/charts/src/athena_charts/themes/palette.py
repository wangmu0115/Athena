from pydantic import Field

from athena_charts.themes._base import _BaseTheme


class PaletteTheme(_BaseTheme):
    sequence: list[str] | None = Field(None, description="默认颜色调色板")
