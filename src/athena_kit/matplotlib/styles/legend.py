from typing import Self

from pydantic import Field

from athena_kit.matplotlib.styles.base import _BaseStyle
from athena_kit.matplotlib.types import LegendLocation


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

    borderpad: float | None = Field(None, ge=0, description="图例内部 padding")
    labelspacing: float | None = Field(None, ge=0, description="图例项垂直间距")
    handlelength: float | None = Field(None, ge=0, description="legend line 长度")
    handleheight: float | None = Field(None, ge=0, description="legend handle 高度")
    handletextpad: float | None = Field(None, ge=0, description="line 与文本间距")
    columnspacing: float | None = Field(None, ge=0, description="列间距")

    markerscale: float | None = Field(None, gt=0, description="marker 缩放比例")

    # # 布局
    # ncols: int | None = Field(None, gt=0, description="图例列数")
    # bbox_to_anchor: tuple[float, float] | None = Field(None, description="图例锚点坐标")

    @classmethod
    def of(
        cls,
        location: LegendLocation = "auto",
        titlesize: int = 6,
        labelsize: int = 4,
        labelcolor: str = "#333333",
        frameon: bool = False,
        framealpha: float = 0.9,
        facecolor: float = "white",
        edgecolor: str = "#DDDDDD",
        shadow: bool = False,
        fancybox: bool = True,
        borderpad: float = 0.25,
        labelspacing: float = 0.35,
        handlelength: float = 1.4,
        handleheight: float = 0.6,
        handletextpad: float = 0.5,
        columnspacing: float = 1.0,
        markerscale: float = 0.8,
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
            borderpad=borderpad,
            labelspacing=labelspacing,
            handlelength=handlelength,
            handleheight=handleheight,
            handletextpad=handletextpad,
            columnspacing=columnspacing,
            markerscale=markerscale,
        )
