from dataclasses import dataclass
from typing import Literal

from matplotlib.axes import Axes

from athena_charts.specs.coords.cartesian import CartesianCoord


@dataclass
class AxesRuntime:
    primary: Axes
    left_y: Axes | None
    right_y: Axes | None
    x_owner: Axes
    grid_owner: Axes | None
    legend_owner: Axes

    def axes_for_y_axis(self, side: Literal["left", "right"]) -> Axes:
        if side == "left":
            if self.left_y is None:
                raise ValueError("Plot requires left y-axis, but left y_axis is not configured.")
            return self.left_y
        if self.right_y is None:
            raise ValueError("Plot requires right y-axis, but right y_axis is not configured.")
        return self.right_y


def resolve_axes_runtime(axes: Axes, coord: CartesianCoord) -> AxesRuntime:
    if coord.left_y_axis is not None and coord.right_y_axis is not None:
        axes_right = axes.twinx()
        return AxesRuntime(
            primary=axes,
            left_y=axes,
            right_y=axes_right,
            x_owner=axes,
            grid_owner=axes,
            legend_owner=axes,
        )
    if coord.left_y_axis is not None:
        return AxesRuntime(
            primary=axes,
            left_y=axes,
            right_y=None,
            x_owner=axes,
            grid_owner=axes,
            legend_owner=axes,
        )
    # Coord only has right Y, set primary axes to right Y.
    axes.yaxis.tick_right()
    axes.yaxis.set_label_position("right")
    return AxesRuntime(
        primary=axes,
        left_y=None,
        right_y=axes,
        x_owner=axes,
        grid_owner=axes,
        legend_owner=axes,
    )
