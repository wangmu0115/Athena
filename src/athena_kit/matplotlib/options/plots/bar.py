from typing import Self

from pydantic import Field, field_serializer

from athena_kit.matplotlib.adapters.styles import to_mpl_hatch_pattern
from athena_kit.matplotlib.options._base import _BaseOptions
from athena_kit.matplotlib.options.plots.data_label import DataLabelOptions
from athena_kit.matplotlib.types import HatchPattern


class BarLayoutOptions(_BaseOptions):
    """柱状图布局运行时配置，用于控制多个 `BarPlot` 在同一个分类位置上如何排列。主要适用于以下柱状图布局模式：

    - group: 分组柱状图，多个柱子在同一个分类下横向并排显示。
    - stack: 堆叠柱状图，多个柱子在同一个分类下沿 Y 轴方向累加。
    - overlay: 覆盖柱状图，多个柱子在同一个分类位置上重叠绘制。

    该配置只描述柱子之间的空间关系，不描述单根柱子的颜色、边框、透明度等视觉样式。
    """

    group_width: float = Field(0.8, description="一组柱子占据分类单位宽度的比例，默认 80%，剩余空间作为组间留白")
    inner_gap: float = Field(0.02, description="分组模式下，同一组内相邻柱子之间的间距，占 X 轴单位宽度的比例")
    separate_positive_negative_stack: bool = Field(True, description="堆叠模式下，是否将正值和负值分别独立堆叠")
    overlay_width_ratio: float = Field(0.8, description="覆盖模式下，后续柱子的宽度缩放比例，用于避免完全遮挡底层柱子")
    overlay_alpha: float = Field(0.8, description="覆盖模式下，重叠柱子的透明度")

    @classmethod
    def default(cls) -> Self:
        """创建默认柱状图布局配置。"""
        return cls.of()

    @classmethod
    def of(
        cls,
        *,
        group_width: float = 0.8,
        inner_gap: float = 0.02,
        separate_positive_negative_stack: bool = True,
        overlay_width_ratio: float = 0.8,
        overlay_alpha: float = 0.8,
    ) -> Self:
        """创建柱状图布局配置。"""
        return cls(
            group_width=group_width,
            inner_gap=inner_gap,
            separate_positive_negative_stack=separate_positive_negative_stack,
            overlay_width_ratio=overlay_width_ratio,
            overlay_alpha=overlay_alpha,
        )


class BarOptions(_BaseOptions):
    """单根柱子的运行时样式配置，用于控制柱子本身的视觉表现，例如填充颜色、边框颜色、边框宽度、透明度和填充纹理。

    该配置通常会作用到 Matplotlib 的 `Axes.bar(...)` 参数。
    """

    color: str | None = Field(None, description="柱子的填充颜色")
    edgecolor: str | None = Field(None, description="柱子的边框颜色")
    linewidth: float | None = Field(None, description="柱子边框线宽")
    alpha: float | None = Field(None, ge=0, le=1, description="柱子的透明度")
    hatch: HatchPattern = Field("none", description="柱子的填充纹理")

    @field_serializer("hatch")
    def serialize_hatch(self, value: HatchPattern) -> str:
        return to_mpl_hatch_pattern(value)


class BarPlotOptions(_BaseOptions):
    """柱状图图层运行时配置，用于描述一个或多个柱状图图层在运行时的绘制行为，包括柱子样式、柱状图布局以及数据标签样式。

    注意：
        - `bar` 控制单根柱子的视觉样式。
        - `layout` 控制多个柱状图图层之间的排列方式。
        - `data_label` 控制柱子上的数值标签。
    """

    bar: BarOptions | None = Field(None, description="柱子样式配置")
    layout: BarLayoutOptions | None = Field(None, description="柱子布局配置")
    data_label: DataLabelOptions | None = Field(None, description="数据标签配置")

    @classmethod
    def of(
        cls,
        *,
        color: str | None = None,
        edgecolor: str | None = None,
        linewidth: float | None = None,
        alpha: float | None = None,
        hatch: HatchPattern = "none",
        layout: BarLayoutOptions | None = None,
        data_label: DataLabelOptions | None = None,
    ) -> Self:
        bar = BarOptions(
            color=color,
            edgecolor=edgecolor,
            linewidth=linewidth,
            alpha=alpha,
            hatch=hatch,
        )
        return cls(
            bar=bar,
            layout=layout or BarLayoutOptions.default(),
            data_label=data_label,
        )
