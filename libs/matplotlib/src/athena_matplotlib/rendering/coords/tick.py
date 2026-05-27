from matplotlib.axis import Axis
from matplotlib.ticker import AutoLocator, FixedLocator, FuncFormatter, MaxNLocator, NullLocator

from athena_matplotlib.specs.coords import TickSpec
from athena_matplotlib.specs.coords.base import AxisSpec
from athena_matplotlib.transforms.tick_labels import format_tick_label
from athena_matplotlib.types.specs import AxisDataType


def render_axis_tick(axis: Axis, spec: AxisSpec):
    if spec.tick is None:
        return
    # Locator
    _render_axis_tick_locator(axis, spec.tick)
    # Formatter
    _render_axis_tick_formatter(axis, spec.tick, data_type=spec.data_type)


def _render_axis_tick_locator(axis: Axis, spec: TickSpec):
    locator = spec.locator
    strategy = locator.strategy

    match strategy:
        case "auto":
            if locator.max_count is not None:
                axis.set_major_locator(MaxNLocator(nbins=locator.max_count))
            else:
                axis.set_major_locator(AutoLocator())
        case "all":
            axis.set_major_locator(AutoLocator())
        case "fixed":
            axis.set_major_locator(FixedLocator(locator.fixed_values or []))
        case "none":
            axis.set_major_locator(NullLocator())
        case _:
            raise ValueError(f"Unsupported tick locator strategy: {strategy}.")


def _render_axis_tick_formatter(axis: Axis, spec: TickSpec, *, data_type: AxisDataType):
    formatter = spec.formatter

    axis.set_major_formatter(
        FuncFormatter(
            lambda value, pos: format_tick_label(
                value,
                formatter,
                axis_data_type=data_type,
            )
        )
    )
