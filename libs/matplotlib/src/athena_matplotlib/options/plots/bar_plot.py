from typing import Literal, Self

from pydantic import Field

from athena_matplotlib.options._base import _BaseOptions
from athena_matplotlib.options.plots.data_label import DataLabelOptions


class BarLayoutOptions(_BaseOptions):
    group_width: float = Field(0.8, description="一组柱子占据分类单位宽度的比例，默认 80% 会为每组柱子之间间隔 10%")
    inner_gap: float = Field(0.05, description="一个分组内，相邻柱子之间的空隙，默认 5% 个 X 轴单位的间距")
    separate_positive_negative_stack: bool = Field(True, description="正值和负值分别独立堆叠")
    overlay_width_ratio: float = Field(0.75, description="覆盖模式下柱宽缩放比例")
    overlay_alpha: float = Field(0.75, description="重叠柱子的透明度")

    @classmethod
    def of(
        cls,
        group_width: float = 0.8,
        inner_gap: float = 0.05,
        separate_positive_negative_stack: bool = True,
        overlay_width_ratio: float = 0.75,
        overlay_alpha: float = 0.75,
    ) -> Self:
        return cls(
            group_width=group_width,
            inner_gap=inner_gap,
            separate_positive_negative_stack=separate_positive_negative_stack,
            overlay_width_ratio=overlay_width_ratio,
            overlay_alpha=overlay_alpha,
        )

    visible: bool = True

    # 几何
    width: float | None = None
    align: Literal["center", "edge"] | None = None

    # 样式
    color: str | None = None
    edgecolor: str | None = None
    linewidth: float | None = None
    alpha: float | None = None
    hatch: str | None = None

    # 布局辅助
    z_index: int | None = None

    # overlay 时很有用
    offset: float | None = None

    # stack 时很有用
    baseline: float | None = None

    # label / legend
    label: str | None = None

    # stack

    # overlay


class BarOptions(_BaseOptions):
    pass


class BarPlotOptions(_BaseOptions):
    bar: BarOptions | None = None
    layout: BarLayoutOptions | None = None
    data_label: DataLabelOptions | None = None
