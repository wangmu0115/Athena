from matplotlib.axes import Axes

from athena_core.values.optional import safe_getattr
from athena_matplotlib.options import LinePlotOptions
from athena_matplotlib.rendering.color_cycle import ColorCycle
from athena_matplotlib.rendering.plots.layers import (
    DataLabelLayerArtist,
    LineLayerArtist,
    MarkerLayerArtist,
)
from athena_matplotlib.rendering.render_plan import AlignedLinePlot


class LineArtist:
    def __init__(self, color_cycle: ColorCycle):
        self._color_cycle = color_cycle
        self._post_init()

    def _post_init(self):
        self._line_layer = LineLayerArtist(self._color_cycle)
        self._marker_layer = MarkerLayerArtist()
        self._datalabel_layer = DataLabelLayerArtist()

    def draw(
        self,
        axes: Axes,
        plot: AlignedLinePlot,
        *,
        options: LinePlotOptions | None,
    ) -> None:
        override = plot.plot.options
        # 1. 绘制折线图
        self._line_layer.draw(
            axes,
            plot.x_values,
            plot.y_values,
            plot_name=plot.plot.name,
            z_index=plot.plot.z_index,
            options=safe_getattr(options, "line"),
            override=safe_getattr(override, "line"),
        )
        # 2. 绘制Marker
        self._marker_layer.draw(
            axes,
            plot.x_values,
            plot.y_values,
            plot_name=plot.plot.name,
            z_index=plot.plot.z_index + 1,
            options=safe_getattr(options, "marker"),
            override=safe_getattr(override, "marker"),
        )
        # 3. 绘制数据标签
        self._datalabel_layer.draw(
            axes,
            plot.x_values,
            plot.y_values,
            plot_name=plot.plot.name,
            z_index=plot.plot.z_index + 1,
            options=safe_getattr(options, "data_label"),
            override=safe_getattr(override, "data_label"),
        )
