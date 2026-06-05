from dataclasses import dataclass
from typing import Literal

from matplotlib.axes import Axes

from athena_kit.matplotlib.specs.coords import CartesianCoord


@dataclass
class AxesRuntime:
    """笛卡尔坐标系运行时 Axes 容器，用于描述一个 Chart 在 Matplotlib 中实际使用的 Axes 拓扑结构。

    说明：
        - `primary` 表示主 Axes，即最初创建的 Axes 实例。
        - `left_y` 表示左侧 Y 轴对应的 Axes。
        - `right_y` 表示右侧 Y 轴对应的 Axes。
        - 当同时存在左右 Y 轴时，`right_y` 通常由 `Axes.twinx()` 创建。
        - 当仅存在右侧 Y 轴时，`primary` 与 `right_y` 指向同一个 Axes。
        - 当仅存在左侧 Y 轴时，`primary` 与 `left_y` 指向同一个 Axes。

    Attributes:
        primary: 主 Axes。
        left_y: 左侧 Y 轴对应的 Axes。
        right_y: 右侧 Y 轴对应的 Axes。
    """

    primary: Axes
    left_y: Axes | None
    right_y: Axes | None

    @property
    def all_axes(self) -> list[Axes]:
        """返回当前 Chart 使用的全部 Axes。"""
        if self.left_y is not None and self.right_y is not None:
            return [self.left_y, self.right_y]
        return [self.primary]

    def axes_for_y_axis(self, side: Literal["left", "right"]) -> Axes:
        """获取指定 Y 轴对应的 Axes。"""
        if side == "left" and self.left_y is not None:
            return self.left_y
        if side == "right" and self.right_y is not None:
            return self.right_y
        raise ValueError(f"Plot requires {side} Y axis, but {side} Y axis is not configured.")


def build_axes_runtime(axes: Axes, coord: CartesianCoord) -> AxesRuntime:
    """根据坐标系配置构建运行时 Axes 拓扑，根据笛卡尔坐标系中的左右 Y 轴配置，创建并返回对应的 :class:`AxesRuntime`。

    拓扑规则：
        1. 同时存在左侧和右侧 Y 轴，创建一个新的右侧 Axes:

        .. code-block:: text
            left_y (primary)
                │
                └── twinx()
                        │
                    right_y

        2. 仅存在左侧 Y 轴:

        .. code-block:: text
            primary == left_y

        3. 仅存在右侧 Y 轴，将主 Axes 调整为右侧刻度模式:

        .. code-block:: text
            primary == right_y
    """
    if coord.left_y_axis is not None and coord.right_y_axis is not None:
        axes_right = axes.twinx()
        return AxesRuntime(primary=axes, left_y=axes, right_y=axes_right)

    if coord.left_y_axis is not None:
        return AxesRuntime(primary=axes, left_y=axes, right_y=None)

    # Coord only has right Y, set primary axes to right Y.
    axes.yaxis.tick_right()
    axes.yaxis.set_label_position("right")
    return AxesRuntime(primary=axes, left_y=None, right_y=axes)
