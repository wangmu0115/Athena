from matplotlib.axes import Axes

from athena_core.values.optional import safe_getattr
from athena_matplotlib.decorations.axis import apply_axis_style
from athena_matplotlib.decorations.grid import apply_grid_style
from athena_matplotlib.decorations.tick import apply_tick_style
from athena_matplotlib.options import CartesianCoordOptions
from athena_matplotlib.rendering.coords._axes_runtime import AxesRuntime
from athena_matplotlib.specs.coords import CartesianCoord
from athena_matplotlib.specs.coords.cartesian import CartesianAxisSpec


def apply_cartesian_style(
    runtime: AxesRuntime,
    coord: CartesianCoord,
    *,
    options: CartesianCoordOptions | None = None,
):
    """
    1. X 和 Y 轴:
        - 缩放、最小值和最大值、标题
        - 坐标轴线可见性和样式
        - 坐标轴刻度线和刻度标签
    2. 网格 Grid
    3. 调整主 Axes 和次 Axes 的坐标轴可见性
    """
    override = coord.options
    # 1.1 X 轴
    apply_x_axis_style(runtime.primary, coord.x_axis, options=options, override=override)
    # 1.2 Y 轴
    if coord.left_y_axis is not None and runtime.left_y is not None:
        apply_y_axis_style(runtime.left_y, coord.left_y_axis, options=options, override=override)
    if coord.right_y_axis is not None and runtime.right_y is not None:
        apply_y_axis_style(runtime.right_y, coord.right_y_axis, options=options, override=override)
    # 2. Grid
    apply_grid_style(
        runtime.primary,
        options=safe_getattr(options, "grid"),
        override=safe_getattr(override, "grid"),
    )
    # 3. 双 Y 轴样式优化
    if runtime.left_y is not None and runtime.right_y is not None:
        runtime.left_y.spines["right"].set_visible(False)

        runtime.right_y.spines["left"].set_visible(False)
        runtime.right_y.spines["top"].set_visible(False)
        runtime.right_y.spines["bottom"].set_visible(False)
        runtime.right_y.tick_params(axis="x", bottom=False, labelbottom=False, top=False, labeltop=False)
        runtime.right_y.grid(False)


def apply_x_axis_style(
    axes: Axes,
    axis: CartesianAxisSpec,
    *,
    options: CartesianCoordOptions | None,
    override: CartesianCoordOptions | None,
):
    # 缩放、最小值和最大值、标题
    axes.set_xscale(axis.scale)
    if axis.min is not None or axis.max is not None:
        axes.set_xlim(axis.min, axis.max)
    if axis.label:
        axes.set_xlabel(axis.label)
    # 设置标签放置的位置
    axes.xaxis.set_label_position(axis.position)
    if axis.position == "bottom":
        axes.xaxis.tick_bottom()
    else:
        axes.xaxis.tick_top()
    # Bottom X axis
    apply_axis_style(
        axes,
        "bottom",
        options=safe_getattr(options, "bottom_axis"),
        override=safe_getattr(override, "bottom_axis"),
    )
    # Top X axis
    apply_axis_style(
        axes,
        "top",
        options=safe_getattr(options, "top_axis"),
        override=safe_getattr(override, "top_axis"),
    )
    # 刻度: top/bottom X
    apply_tick_style(
        axes,
        axis.position,
        options=safe_getattr(options, f"{axis.position}_tick"),
        override=safe_getattr(override, f"{axis.position}_tick"),
    )


def apply_y_axis_style(
    axes: Axes,
    axis: CartesianAxisSpec,
    *,
    options: CartesianCoordOptions | None,
    override: CartesianCoordOptions | None,
):
    # 缩放、最小值和最大值、坐标轴标题
    axes.set_yscale(axis.scale)
    if axis.min is not None or axis.max is not None:
        axes.set_ylim(axis.min, axis.max)
    if axis.label:
        axes.set_ylabel(axis.label)
    # 设置标签放置的位置
    axes.yaxis.set_label_position(axis.position)
    if axis.position == "left":
        axes.yaxis.tick_left()
    else:
        axes.yaxis.tick_right()
    # 轴线
    apply_axis_style(
        axes,
        axis.position,
        options=safe_getattr(options, f"{axis.position}_axis"),
        override=safe_getattr(override, f"{axis.position}_axis"),
    )
    # 刻度
    apply_tick_style(
        axes,
        axis.position,
        options=safe_getattr(options, f"{axis.position}_tick"),
        override=safe_getattr(override, f"{axis.position}_tick"),
    )
