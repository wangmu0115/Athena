import uuid

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec

from athena_charts.runtime import BaseRenderer, RenderResult
from athena_charts.specs.figures import FigureSpec
from athena_charts.specs.figures.layout import FigureGridLayout
from athena_charts_matplotlib.artifact import MatplotlibFigureArtifact
from athena_charts_matplotlib.rendering.context import matplotlib_theme_context
from athena_charts_matplotlib.rendering.options import MatplotlibRenderOptions
from athena_charts_matplotlib.styles import MatplotlibStyle
from athena_core.values.optional import optional_map_or, safe_getattr


class MatplotlibFigureRenderer(BaseRenderer[MatplotlibFigureArtifact]):
    def __init__(
        self,
        name: str = "",
        *,
        style: MatplotlibStyle | None = None,
        options: MatplotlibRenderOptions | None = None,
    ):
        super().__init__(name=name or uuid.uuid())
        self._style = style or MatplotlibStyle.default()
        self._options = options or MatplotlibRenderOptions.default()

    @property
    def style(self):
        return self._style

    @property
    def options(self):
        return self._options

    def _render_figure(self, spec: FigureSpec) -> RenderResult[MatplotlibFigureArtifact]:
        with matplotlib_theme_context(self.style):
            # Figure
            figure = self._create_figure(spec)
            # Layout
            gs = self._add_gridspec(figure, spec.layout)
            # Render Charts
            for chart_placement in spec.charts:
                row = (chart_placement.row or 1) - 1
                col = (chart_placement.col or 1) - 1
                axes = figure.add_subplot(gs[row : row + chart_placement.row_span, col : col + chart_placement.col_span])
                self._chart_renderer.render(axes, chart_placement.chart, context=render_context)

        artifact = MatplotlibFigureArtifact(figure, options=self.options.save_figure)
        return RenderResult(
            artifact=artifact,
            metadata={"renderer": self.name},
        )

    def _create_figure(self, spec: FigureSpec) -> Figure:
        fig: Figure = plt.figure(
            **optional_map_or(
                self.options.figure,
                lambda x: x.build_create_params,
                default={},
            )
        )
        title = safe_getattr(spec.labels, "title")
        if title:
            fig.suptitle(
                title,
                **optional_map_or(
                    self.options.figure,
                    lambda x: x.build_title_params,
                    default={},
                ),
            )
        return fig

    def _add_gridspec(self, figure: Figure, layout: FigureGridLayout) -> GridSpec:
        if layout is None or layout.rows is None or layout.cols is None:
            raise ValueError("FigureSpec.layout must be resolved before rendering.")
        gridspec_params: dict[str, object] = {}
        if layout.hspace is not None:
            gridspec_params["hspace"] = layout.hspace
        if layout.wspace is not None:
            gridspec_params["wspace"] = layout.wspace

        return figure.add_gridspec(nrows=layout.rows, ncols=layout.cols, **gridspec_params)
