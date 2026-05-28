from typing import Literal

from pydantic import Field

from athena_matplotlib.options._base import _BaseOptions
from athena_matplotlib.options.data_label import DataLabelOptions


class BarLayoutOptions(_BaseOptions):
    group_width: float = Field(0.8, description="一组柱子占据分类单位宽度的比例，默认 80% 会为每组柱子之间间隔 10%")
    inner_gap: float = Field(0.05, description="一个分组内，相邻柱子之间的空隙，默认 5% 个 X 轴单位的间距")

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
    stack_positive_negative_separately: bool = True

    # overlay
    overlay_width_ratio: float = 0.75
    overlay_alpha: float | None = 0.75


class BarPlotOptions(_BaseOptions):
    bar_layer: BarLayoutOptions | None = None
    data_label: DataLabelOptions | None = None
