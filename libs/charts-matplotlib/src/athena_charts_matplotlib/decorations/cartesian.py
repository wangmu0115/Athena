from typing import Literal

import matplotlib as mpl
from matplotlib.axes import Axes

from athena_charts.specs.coords.cartesian import CartesianAxisSpec, CartesianCoord
from athena_charts_matplotlib.adapters.axes import AxesRuntime
from athena_charts_matplotlib.adapters.styles import to_mpl_axis_scale
from athena_charts_matplotlib.rendering.options.chart import ChartOptions
from athena_charts_matplotlib.rendering.options.coord import AxesOptions, AxisOptions
from athena_core.values.fallbacks import first_not_none
from athena_core.values.optional import optional_map, safe_getattr


def apply_coord(
    runtime: AxesRuntime,
    coord: CartesianCoord,
    *,
    default_options: ChartOptions | None,
    override_options: ChartOptions | None,
):
    pass


def apply_x_axis_style(
    axes: Axes,
    axis: CartesianAxisSpec,
    *,
    default_options: AxesOptions,
    override_options: AxesOptions,
):
    """
    label: str = Field("", description="坐标轴标题")
    data_type: AxisDataType = Field("number", description="坐标轴数据类型")
    scale: AxisScale = Field("linear", description="坐标轴缩放方式。")
    domain_min: object | None = Field(None, description="坐标轴数据域最小值，类型应与坐标轴数据类型兼容。")
    domain_max: object | None = Field(None, description="坐标轴数据域最大值，类型应与坐标轴数据类型兼容。")
    tick: TickSpec = Field(default_factory=TickSpec, description="坐标轴配置项")
    """
    axes.set_xscale(to_mpl_axis_scale(axis.scale))
    if axis.domain_min is not None or axis.domain_max is not None:
        axes.set_xlim(axis.domain_min, axis.domain_max)
    if axis.label:
        axes.set_xlabel(axis.label)


def _apply_axes_ownership(
    axes: Axes,
    loc: Literal["top", "bottom", "left", "right"],
    *,
    default_options: ChartOptions | None,
    override_options: ChartOptions | None,
):
    """统一处理双轴时的 spine/tick/grid ownership."""
    pass


def apply_axis(
    axes: Axes,
    loc: Literal["top", "bottom", "left", "right"],
    label: str | None,
    *,
    default_options: AxisOptions | None,
    override_options: AxisOptions | None,
) -> bool:
    # Spine
    visible = first_not_none(
        safe_getattr(default_options, "visible"),
        safe_getattr(override_options, "visible"),
        mpl.rcParams[f"axes.spines.{loc}"],
    )
    axes.spines[loc].set_visible(visible)
    if visible:
        spine_params = optional_map(default_options, lambda x: x.build_spine_params)
        spine_params.update(optional_map(override_options, lambda x: x.build_spine_params))
        if spine_params:
            axes.spines[loc].set(**spine_params)
    # Axis label
    if label:
        axes.set_xlabel()

    return visible
