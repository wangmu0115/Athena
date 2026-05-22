from pydantic import Field

from athena_charts_matplotlib.styles._base import _BaseStyle


class MatplotlibPaletteStyle(_BaseStyle):
    sequence: list[str] | None = Field(None, description="默认颜色调色板")
