from typing import Self

from pydantic import Field

from athena_charts.themes import FontWeight
from athena_charts_matplotlib.styles.base import _BaseStyle


class FigureStyle(_BaseStyle):
    size: tuple[int, int] | None = Field(None, description="画布大小: (width, height)")
    dpi: int | None = Field(None, gt=0, description="分辨率，每英寸点数")
    facecolor: str | None = Field(None, description="画布背景颜色")
    edgecolor: str | None = Field(None, description="画布边框颜色")

    titlesize: int | None = Field(None, gt=0, description="画布标题字号")
    titleweight: FontWeight | None = Field(None, description="画布标题字体粗细")

    @classmethod
    def default(cls) -> Self:
        return cls.of()

    @classmethod
    def of(
        cls,
        size: tuple[int, int] = (960, 720),
        dpi: int = 150,
        facecolor: str = "white",
        edgecolor: str = "white",
        titlesize: int = 12,
        titleweight: FontWeight = "normal",
    ) -> Self:
        return cls(
            size=size,
            dpi=dpi,
            facecolor=facecolor,
            edgecolor=edgecolor,
            titlesize=titlesize,
            titleweight=titleweight,
        )
