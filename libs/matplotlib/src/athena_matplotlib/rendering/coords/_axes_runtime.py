from dataclasses import dataclass
from typing import Literal

from matplotlib.axes import Axes

from athena_matplotlib.specs.coords import CartesianCoord


@dataclass
class AxesRuntime:
    primary: Axes
    left_y: Axes | None
    right_y: Axes | None

    @property
    def all_axes(self) -> list[Axes]:
        if self.left_y is not None and self.right_y is not None:
            return [self.left_y, self.right_y]
        return [self.primary]

    def axes_for_y_axis(self, side: Literal["left", "right"]) -> Axes:
        if side == "left" and self.left_y is not None:
            return self.left_y
        if side == "right" and self.right_y is not None:
            return self.right_y
        raise ValueError(f"Plot requires {side} Y axis, but {side} Y axis is not configured.")


def resolve_axes_runtime(axes: Axes, coord: CartesianCoord) -> AxesRuntime:
    if coord.left_y_axis is not None and coord.right_y_axis is not None:
        axes_right = axes.twinx()
        return AxesRuntime(primary=axes, left_y=axes, right_y=axes_right)

    if coord.left_y_axis is not None:
        return AxesRuntime(primary=axes, left_y=axes, right_y=None)

    # Coord only has right Y, set primary axes to right Y.
    axes.yaxis.tick_right()
    axes.yaxis.set_label_position("right")
    return AxesRuntime(primary=axes, left_y=None, right_y=axes)
