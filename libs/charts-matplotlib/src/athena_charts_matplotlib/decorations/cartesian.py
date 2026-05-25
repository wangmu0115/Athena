from typing import Literal

from matplotlib.axes import Axes

from athena_charts.specs.coords.cartesian import CartesianAxisSpec, CartesianCoord
from athena_charts_matplotlib.adapters.axes import AxesRuntime
from athena_charts_matplotlib.adapters.styles import to_mpl_axis_scale
from athena_charts_matplotlib.rendering.options.chart import ChartOptions
from athena_charts_matplotlib.rendering.options.coord import AxisOptions, CoordOptions, TickOptions
from athena_core.values.fallbacks import first_not_none
from athena_core.values.optional import optional_map_or, safe_getattr


def apply_coord_style(
    runtime: AxesRuntime,
    coord: CartesianCoord,
    *,
    default_options: ChartOptions | None,
    override_options: ChartOptions | None,
):
    """"""
    # X 轴的配置在 X Axis Owner 上配置
    default_coord_options: CoordOptions = safe_getattr(default_options, "coord")
    override_coord_options: CoordOptions = safe_getattr(override_options, "coord")
    apply_x_axis_style(
        runtime.x_owner,
        coord.x_axis,
        default_options=default_coord_options,
        override_options=override_coord_options,
    )
    # Left Y 轴的配置
    if coord.left_y_axis is not None and runtime.left_y is not None:
        apply_y_axis_style(
            runtime.axes_for_y_axis("left"),
            coord.left_y_axis,
            "left",
            default_options=default_coord_options,
            override_options=override_coord_options,
        )
    # Right Y 轴的配置
    if coord.right_y_axis is not None and runtime.right_y is not None:
        apply_y_axis_style(
            runtime.axes_for_y_axis("right"),
            coord.right_y_axis,
            "right",
            default_options=default_options,
            override_options=override_options,
        )
    # Grid 配置
    default_grid_options: CoordOptions = safe_getattr(default_options, "coord")
    override_grid_options: CoordOptions = safe_getattr(override_options, "coord")
    apply_grid_style(
        runtime.grid_owner,
        default_options=default_grid_options,
        override_options=override_grid_options,
    )
    # 根据是否具有两个 Y 轴，优化轴线的展示
    if runtime.left_y is not None and runtime.right_y is not None:
        runtime.left_y.spines["right"].set_visible(False)

        runtime.right_y.spines["left"].set_visible(False)
        runtime.right_y.spines["top"].set_visible(False)
        runtime.right_y.spines["bottom"].set_visible(False)
        runtime.right_y.tick_params(
            axis="x",
            bottom=False,
            labelbottom=False,
            top=False,
            labeltop=False,
        )
        runtime.right_y.grid(False)


def apply_x_axis_style(
    axes: Axes,
    axis: CartesianAxisSpec,
    *,
    default_options: CoordOptions | None,
    override_options: CoordOptions | None,
):
    # 缩放、最小值和最大值、坐标轴标题
    axes.set_xscale(to_mpl_axis_scale(axis.scale))
    if axis.domain_min is not None or axis.domain_max is not None:
        axes.set_xlim(axis.domain_min, axis.domain_max)
    if axis.label:
        axes.set_xlabel(axis.label)
    # 轴线配置: top X & bottom X
    _apply_axis_spine_label_style(axes, "bottom", default_options=default_options, override_options=override_options)
    _apply_axis_spine_label_style(axes, "top", default_options=default_options, override_options=override_options)
    # 刻度配置: top X & bottom X
    _apply_axis_tick_style(axes, "bottom", default_options=default_options, override_options=override_options)
    _apply_axis_tick_style(axes, "top", default_options=default_options, override_options=override_options)


def apply_y_axis_style(
    axes: Axes,
    axis: CartesianAxisSpec,
    loc: Literal["left", "right"],
    *,
    default_options: CoordOptions | None,
    override_options: CoordOptions | None,
):
    # 缩放、最小值和最大值、坐标轴标题
    axes.set_yscale(to_mpl_axis_scale(axis.scale))
    if axis.domain_min is not None or axis.domain_max is not None:
        axes.set_ylim(axis.domain_min, axis.domain_max)
    if axis.label:
        axes.set_ylabel(axis.label)
    # 设置标签放置的位置
    axes.yaxis.set_label_position(loc)
    if loc == "left":
        axes.yaxis.tick_left()
    else:
        axes.yaxis.tick_right()
    # 轴线配置: Y
    _apply_axis_spine_label_style(axes, loc, default_options=default_options, override_options=override_options)
    # Tick 配置
    _apply_axis_tick_style(axes, loc, default_options=default_options, override_options=override_options)


def apply_grid_style(axes: Axes, *, default_options: ChartOptions | None, override_options: ChartOptions | None):
    visible = first_not_none(
        safe_getattr(default_options, "visible"),
        safe_getattr(override_options, "visible"),
        default=True,
    )
    if not visible:
        axes.grid(False)
    else:
        params = optional_map_or(default_options, lambda x: x.build_grid_params(), default={})
        params.update(optional_map_or(override_options, lambda x: x.build_grid_params(), default={}))
        axes.grid(True, **params)


def _apply_axis_spine_label_style(
    axes: Axes,
    loc: Literal["top", "bottom", "left", "right"],
    *,
    default_options: CoordOptions | None,
    override_options: CoordOptions | None,
):
    default_axis_options: AxisOptions = safe_getattr(default_options, f"{loc}_axis")
    override_axis_options: AxisOptions = safe_getattr(override_options, f"{loc}_axis")
    # Spine
    spine_params = optional_map_or(default_axis_options, lambda x: x.build_spine_params(), default={})
    spine_params.update(optional_map_or(override_axis_options, lambda x: x.build_spine_params(), default={}))
    axes.spines[loc].set(**spine_params)
    # Label
    label_params = optional_map_or(default_axis_options, lambda x: x.build_label_params(), default={})
    label_params.update(optional_map_or(override_axis_options, lambda x: x.build_label_params(), default={}))
    if loc in {"top", "bottom"}:
        axes.xaxis.label.set(**label_params)
    if loc in {"left", "right"}:
        axes.yaxis.label.set(**label_params)


def _apply_axis_tick_style(
    axes: Axes,
    loc: Literal["top", "bottom", "left", "right"],
    *,
    default_options: CoordOptions | None,
    override_options: CoordOptions | None,
):
    default_tick_options: TickOptions = safe_getattr(default_options, f"{loc}_tick")
    override_tick_options: TickOptions = safe_getattr(override_options, f"{loc}_tick")
    # Tick
    axis = "x" if loc in {"top", "bottom"} else "y"
    line_visible = first_not_none(
        safe_getattr(safe_getattr(default_tick_options, "line"), "visible"),
        safe_getattr(safe_getattr(override_tick_options, "line"), "visible"),
        default=True,
    )
    label_visible = first_not_none(
        safe_getattr(safe_getattr(default_tick_options, "label"), "visible"),
        safe_getattr(safe_getattr(override_tick_options, "label"), "visible"),
        default=True,
    )
    # Tick line params
    tick_line_params = optional_map_or(default_tick_options, lambda x: x.build_line_params(), default={})
    tick_line_params.update(optional_map_or(override_tick_options, lambda x: x.build_line_params(), default={}))
    # Tick label params
    tick_label_params = optional_map_or(default_tick_options, lambda x: x.build_label_params(), default={})
    tick_label_params.update(optional_map_or(override_tick_options, lambda x: x.build_label_params(), default={}))
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


def _apply_axes_ownership(runtime: AxesRuntime, coord: CartesianCoord):
    """统一处理双轴时的 spine/tick/grid ownership."""
    primary = runtime.primary
    if runtime.left_y is not None and runtime.right_y is not None:
        primary.spines["right"].set_visible(False)

        ax_right = runtime.right_y
        ax_right.spines["top"].set_visible(False)
        ax_right.spines["left"].set_visible(False)
        ax_right.spines["bottom"].set_visible(False)

        ax_right.tick_params(
            axis="x",
            bottom=False,
            labelbottom=False,
            top=False,
            labeltop=False,
        )
        ax_right.grid(False)
