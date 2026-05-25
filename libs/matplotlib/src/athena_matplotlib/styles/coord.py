from typing import Self

from pydantic import Field

from athena_matplotlib.styles.base import _BaseStyle
from athena_matplotlib.types import FontWeight


class AxisStyle(_BaseStyle):
    linewidth: float | None = Field(None, gt=0, description="坐标轴线宽")
    linecolor: str | None = Field(None, description="坐标轴线颜色")
    labelsize: int | None = Field(None, gt=0, description="坐标轴标题字号")
    labelweight: FontWeight | None = Field(None, description="坐标轴标题粗细")
    labelcolor: str | None = Field(None, description="坐标轴标题颜色")

    @classmethod
    def of(
        cls,
        linewidth: float = 0.6,
        linecolor: str = "#333333",
        labelsize: int = 6,
        labelweight: FontWeight = "normal",
        labelcolor: str = "#111111",
    ) -> Self:
        return cls(
            linewidth=linewidth,
            linecolor=linecolor,
            labelsize=labelsize,
            labelweight=labelweight,
            labelcolor=labelcolor,
        )
