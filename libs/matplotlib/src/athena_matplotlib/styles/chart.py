from typing import Self

from pydantic import Field

from athena_matplotlib.styles.base import _BaseStyle
from athena_matplotlib.types.styles import FontWeight


class ChartStyle(_BaseStyle):
    facecolor: str | None = Field(None, description="背景颜色")
    titlesize: int | None = Field(None, gt=0, description="标题字号")
    titleweight: FontWeight | None = Field(None, description="标题字体粗细")
    titlecolor: str | None = Field(None, description="标题字体颜色")

    @classmethod
    def of(
        cls,
        facecolor: str = "white",
        titlesize: int = 10,
        titleweight: FontWeight = "normal",
        titlecolor: str = "#111111",
    ) -> Self:
        return cls(
            facecolor=facecolor,
            titlesize=titlesize,
            titleweight=titleweight,
            titlecolor=titlecolor,
        )
