from typing import Protocol

from matplotlib.axes import Axes

from athena_charts.specs.coords.unions import CoordSpec
from athena_charts.specs.plots import PlotSpec


class PlotArtist(Protocol):
    kind: str

    def draw(
        self,
        axes: Axes,
        plot: PlotSpec,
        *,
        coord: CoordSpec,
    ) -> None: ...
