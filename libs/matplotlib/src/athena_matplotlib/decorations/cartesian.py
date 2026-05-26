from typing import Literal

from matplotlib.axes import Axes

from athena_core.values.fallbacks import first_not_none
from athena_core.values.optional import optional_map_or, safe_getattr
from athena_matplotlib.options import AxisOptions, CartesianCoordOptions, GridOptions, TickOptions
from athena_matplotlib.rendering.coords.axes_runtime import AxesRuntime
from athena_matplotlib.specs.coords import CartesianCoord
from athena_matplotlib.specs.coords.cartesian import CartesianAxisSpec


def apply_cartesian_style(runtime: AxesRuntime, coord: CartesianCoord, *, options: CartesianCoordOptions):
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
    apply_grid_style(runtime.primary, options=options, override=override)
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
    # 轴线
    _apply_axis_spine_label_style(axes, "bottom", options=options, override=override)
    _apply_axis_spine_label_style(axes, "top", options=options, override=override)
    # 刻度: top/bottom X
    _apply_axis_tick_style(axes, axis.position, options=options, override=override)


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
    _apply_axis_spine_label_style(axes, axis.position, options=options, override=override)
    # 刻度
    _apply_axis_tick_style(axes, axis.position, options=options, override=override)


def apply_grid_style(
    axes: Axes,
    *,
    options: CartesianCoordOptions | None,
    override: CartesianCoordOptions | None,
):
    grid_options: GridOptions = safe_getattr(options, "grid")
    override_grid: GridOptions = safe_getattr(override, "grid")

    visible = first_not_none(
        safe_getattr(override_grid, "visible"),
        safe_getattr(grid_options, "visible"),
        default=True,
    )
    if not visible:
        axes.grid(False)
    else:
        params = optional_map_or(grid_options, lambda x: x.build_grid_params(), default={})
        params.update(optional_map_or(override_grid, lambda x: x.build_grid_params(), default={}))
        axes.grid(True, **params)


def _apply_axis_spine_label_style(
    axes: Axes,
    loc: Literal["top", "bottom", "left", "right"],
    *,
    options: CartesianCoordOptions | None,
    override: CartesianCoordOptions | None,
):
    axis_options: AxisOptions = safe_getattr(options, f"{loc}_axis")
    override_axis: AxisOptions = safe_getattr(override, f"{loc}_axis")
    # Spine
    spine_params = optional_map_or(axis_options, lambda x: x.build_spine_params(), default={})
    spine_params.update(optional_map_or(override_axis, lambda x: x.build_spine_params(), default={}))
    axes.spines[loc].set(**spine_params)
    # Label
    label_params = optional_map_or(axis_options, lambda x: x.build_label_params(), default={})
    label_params.update(optional_map_or(override_axis, lambda x: x.build_label_params(), default={}))
    if loc in {"top", "bottom"}:
        axes.xaxis.label.set(**label_params)
    if loc in {"left", "right"}:
        axes.yaxis.label.set(**label_params)


def _apply_axis_tick_style(
    axes: Axes,
    loc: Literal["top", "bottom", "left", "right"],
    *,
    options: CartesianCoordOptions | None,
    override: CartesianCoordOptions | None,
):
    tick_options: TickOptions = safe_getattr(options, f"{loc}_tick")
    override_tick: TickOptions = safe_getattr(override, f"{loc}_tick")
    # Tick
    axis = "x" if loc in {"top", "bottom"} else "y"
    line_visible = first_not_none(
        safe_getattr(safe_getattr(tick_options, "line"), "visible"),
        safe_getattr(safe_getattr(override_tick, "line"), "visible"),
        default=True,
    )
    label_visible = first_not_none(
        safe_getattr(safe_getattr(tick_options, "label"), "visible"),
        safe_getattr(safe_getattr(override_tick, "label"), "visible"),
        default=True,
    )
    # Tick line params
    tick_line_params = optional_map_or(tick_options, lambda x: x.build_line_params(), default={})
    tick_line_params.update(optional_map_or(override_tick, lambda x: x.build_line_params(), default={}))
    # Tick label params
    tick_label_params = optional_map_or(tick_options, lambda x: x.build_label_params(), default={})
    tick_label_params.update(optional_map_or(override_tick, lambda x: x.build_label_params(), default={}))
    # Full Params
    params = {
        "axis": axis,
        f"{loc}": line_visible,
        f"label{loc}": label_visible,
    }
    if tick_line_params:
        params.update(**tick_line_params)
    if tick_label_params:
        params.update(**tick_label_params)
    # 更新 Tick 运行时渲染参数
    axes.tick_params(**params)
