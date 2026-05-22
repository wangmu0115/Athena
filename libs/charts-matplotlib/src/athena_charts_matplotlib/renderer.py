import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec

from athena_charts.options.figure import FigureOptions
from athena_charts.runtime import BaseRenderer, RenderResult
from athena_charts.specs.figures import FigureSpec
from athena_charts.specs.figures.layout import FigureGridLayout
from athena_charts.themes import Theme
from athena_charts_matplotlib.artifact import MatplotlibFigureArtifact
from athena_charts_matplotlib.charts.renderer import MatplotlibChartRenderer
from athena_charts_matplotlib.options import DEFAULT_MATPLOTLIB_OPTIONS, MatplotlibOptions
from athena_charts_matplotlib.rendering.context import MatplotlibRenderContext, matplotlib_theme_context
from athena_core.values.optional import optional_map, safe_getattr


class MatplotlibRenderer(BaseRenderer[MatplotlibFigureArtifact]):
    def __init__(self, name: str = "", theme: Theme | None = None, *, options: MatplotlibOptions | None = None):
        super().__init__(name=name, theme=theme)
        self._options = options or DEFAULT_MATPLOTLIB_OPTIONS
        self._chart_renderer = MatplotlibChartRenderer()

    @property
    def options(self):
        return self._options

    def _render_figure(self, spec: FigureSpec) -> RenderResult[MatplotlibFigureArtifact]:
        with matplotlib_theme_context(self.theme, self.options):
            # Figure
            figure = self._create_figure(spec.options)
            # suptitle
            title = optional_map(spec.labels, lambda x: x.title)
            if title is not None:
                figure.suptitle(title)
            # layout
            gs = self._add_gridspec(figure, spec.layout)
            # Render Charts
            render_context = MatplotlibRenderContext(self.theme, self.options)
            for chart_placement in spec.charts:
                row = (chart_placement.row or 1) - 1
                col = (chart_placement.col or 1) - 1
                axes = figure.add_subplot(gs[row : row + chart_placement.row_span, col : col + chart_placement.col_span])
                self._chart_renderer.render(axes, chart_placement.chart, context=render_context)

        artifact = MatplotlibFigureArtifact(
            figure,
            options=optional_map(self._options, lambda x: x.saving),
        )
        return RenderResult(
            artifact=artifact,
            metadata={"renderer": self.name},
        )

    def _create_figure(self, options: FigureOptions | None) -> Figure:
        width, height = safe_getattr(options, "width"), safe_getattr(options, "height")
        if width is not None and height is not None:
            dpi = mpl.rcParams["figure.dpi"]
            return plt.figure(figsize=(width / dpi, height / dpi), dpi=dpi)
        return plt.figure()

    def _add_gridspec(self, figure: Figure, layout: FigureGridLayout) -> GridSpec:
        if layout is None or layout.rows is None or layout.cols is None:
            raise ValueError("FigureSpec.layout must be resolved before rendering.")
        gridspec_params: dict[str, object] = {}
        if layout.hspace is not None:
            gridspec_params["hspace"] = layout.hspace
        if layout.wspace is not None:
            gridspec_params["wspace"] = layout.wspace

        return figure.add_gridspec(nrows=layout.rows, ncols=layout.cols, **gridspec_params)
