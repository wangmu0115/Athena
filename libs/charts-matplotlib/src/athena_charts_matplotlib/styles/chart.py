from typing import Self

from pydantic import Field

from athena_charts_matplotlib.styles.base import _BaseStyle
from athena_charts_matplotlib.styles.types import FontWeight


class AxisLineVisible(_BaseStyle):
    top: bool | None = Field(None, description="顶部轴线是否显示")
    bottom: bool | None = Field(None, description="底部轴线是否显示")
    left: bool | None = Field(None, description="左侧轴线是否显示")
    right: bool | None = Field(None, description="右侧轴线是否显示")

    @classmethod
    def all_visible(cls) -> Self:
        return cls.of()

    @classmethod
    def all_hide(cls) -> Self:
        return cls.of(top=False, bottom=False, left=False, right=False)

    @classmethod
    def classic(cls) -> Self:
        return cls.of(top=False, bottom=True, left=True, right=False)

    @classmethod
    def of(
        cls,
        top: bool = True,
        bottom: bool = True,
        left: bool = True,
        right: bool = True,
    ) -> Self:
        return cls(
            top=top,
            bottom=bottom,
            left=left,
            right=right,
        )


class ChartStyle(_BaseStyle):
    facecolor: str | None = Field(None, description="背景颜色")

    titlesize: int | None = Field(None, gt=0, description="标题字号")
    titleweight: FontWeight | None = Field(None, description="标题字体粗细")
    titlecolor: str | None = Field(None, description="标题字体颜色")

    axis_line_visible: AxisLineVisible | None = Field(None, description="坐标轴线显示配置")

    @classmethod
    def default(cls) -> Self:
        return cls.of()

    @classmethod
    def of(
        cls,
        facecolor: str = "white",
        titlesize: int = 10,
        titleweight: FontWeight = "normal",
        titlecolor: str = "#111111",
        axis_line_visible: AxisLineVisible | None = None,
    ) -> Self:
        return cls(
            facecolor=facecolor,
            titlesize=titlesize,
            titleweight=titleweight,
            titlecolor=titlecolor,
            axis_line_visible=axis_line_visible or AxisLineVisible.all_visible(),
        )
