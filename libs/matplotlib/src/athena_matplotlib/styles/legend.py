from typing import Self

from pydantic import Field

from athena_matplotlib.styles.base import _BaseStyle
from athena_matplotlib.types import LegendLocation


class LegendStyle(_BaseStyle):
    location: LegendLocation | None = Field(None, description="图例位置")

    titlesize: int | None = Field(None, gt=0, description="图例标题字号")

    labelsize: int | None = Field(None, gt=0, description="图例文本字号")
    labelcolor: str | None = Field(None, description="图例文本颜色")

    frameon: bool | None = Field(None, description="是否显示边框")
    framealpha: float | None = Field(None, ge=0, le=1, description="图例透明度")
    facecolor: str | None = Field(None, description="图例背景颜色")
    edgecolor: str | None = Field(None, description="图例边框颜色")
    shadow: bool | None = Field(None, description="是否有阴影")
    fancybox: bool | None = Field(None, description="圆角边框")

    @classmethod
    def of(
        cls,
        location: LegendLocation = "auto",
        titlesize: int = 6,
        labelsize: int = 4,
        labelcolor: str = "#111111",
        frameon: bool = True,
        framealpha: float = 0.8,
        facecolor: float = "white",
        edgecolor: str = "#333333",
        shadow: bool = False,
        fancybox: bool = True,
    ) -> Self:
        return cls(
            location=location,
            titlesize=titlesize,
            labelsize=labelsize,
            labelcolor=labelcolor,
            frameon=frameon,
            framealpha=framealpha,
            facecolor=facecolor,
            edgecolor=edgecolor,
            shadow=shadow,
            fancybox=fancybox,
        )
