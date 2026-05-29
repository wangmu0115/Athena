from collections.abc import Sequence

from matplotlib.axis import Axis
from matplotlib.ticker import AutoLocator, FixedLocator, FuncFormatter, MaxNLocator, NullLocator

from athena_core.values.fallbacks import first_not_none
from athena_matplotlib.rendering.coords._render_plan import AxisTickContext
from athena_matplotlib.specs.coords import TickSpec
from athena_matplotlib.specs.coords.base import AxisSpec
from athena_matplotlib.transforms.tick_labels import format_tick_label
from athena_matplotlib.types.specs import AxisDataType


def render_axis_tick(axis: Axis, spec: AxisSpec, *, context: AxisTickContext | None = None):
    if spec.tick is None:
        return
    # Locator
    _render_axis_tick_locator(axis, spec.tick, data_type=spec.data_type, context=context)
    # Formatter
    _render_axis_tick_formatter(axis, spec.tick, data_type=spec.data_type, context=context)


def _render_axis_tick_locator(
    axis: Axis,
    spec: TickSpec,
    *,
    data_type: AxisDataType,
    context: AxisTickContext | None = None,
):
    locator = spec.locator
    strategy = locator.strategy

    if data_type == "category":
        if context is None:
            raise ValueError("Category axis requires AxisTickContext.")
        match strategy:
            case "auto":
                max_count = first_not_none(locator.max_count, default=8)
                positions = _sample_tick_positions(context.positions, max_count=max_count)
                axis.set_major_locator(FixedLocator(positions))
            case "all":
                axis.set_major_locator(FixedLocator(context.positions))
            case "fixed":
                axis.set_major_locator(FixedLocator(locator.fixed_values or []))
            case "none":
                axis.set_major_locator(NullLocator())
            case _:
                raise ValueError(f"Unsupported tick locator strategy: {strategy}.")
    else:
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


def _render_axis_tick_formatter(
    axis: Axis,
    spec: TickSpec,
    *,
    data_type: AxisDataType,
    context: AxisTickContext | None = None,
):
    formatter = spec.formatter

    if data_type == "category":
        if context is None:
            raise ValueError("Category axis requires AxisTickContext.")
        value_by_position = {
            round(position, 10): value
            for position, value in zip(
                context.positions,
                context.values,
                strict=True,
            )
        }
        axis.set_major_formatter(
            FuncFormatter(
                lambda value, pos: format_tick_label(
                    value_by_position.get(round(value, 10), ""),
                    formatter,
                    axis_data_type=data_type,
                )
            )
        )
    else:
        axis.set_major_formatter(
            FuncFormatter(
                lambda value, pos: format_tick_label(
                    value,
                    formatter,
                    axis_data_type=data_type,
                )
            )
        )


def _sample_tick_positions(positions: Sequence[float], *, max_count: int) -> list[float]:
    if max_count <= 0:
        return []

    if len(positions) <= max_count:
        return list(positions)

    if max_count == 1:
        return [positions[0]]

    step = (len(positions) - 1) / (max_count - 1)
    indexes = {round(i * step) for i in range(max_count)}
    return [positions[index] for index in sorted(indexes)]
