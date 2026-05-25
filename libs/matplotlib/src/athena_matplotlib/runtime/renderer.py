import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec

import matplotlib as mpl
from athena_core.values.optional import optional_map_or
from athena_matplotlib.options import RenderFigureOptions
from athena_matplotlib.rendering.chart import ChartRenderer
from athena_matplotlib.runtime.context import build_rc_params
from athena_matplotlib.specs import ChartSpec, FigureSpec
from athena_matplotlib.specs.figure import FigureGridLayout
from athena_matplotlib.styles import Theme

type RenderSpec = ChartSpec | FigureSpec


@dataclass
class RenderResult:
    figure: Figure
    """Matplotlib `Figure`"""
    metadata: dict[str, object] = field(default_factory=dict)
    """元数据信息"""


class BaseRenderer(ABC):
    def __init__(self, name: str, *, theme: Theme):
        self._name = name  # tracing
        self._theme = theme

    @property
    def name(self) -> str:
        return self._name

    @property
    def theme(self) -> str:
        return self._theme

    def render(self, spec: RenderSpec, *, options: RenderFigureOptions | None) -> RenderResult:
        figure_spec = FigureSpec.from_chart(spec) if isinstance(spec, ChartSpec) else spec
        return self._render_figure(
            figure_spec,
            options=options or RenderFigureOptions.default(),
        )

    @abstractmethod
    def _render_figure(self, spec: FigureSpec, *, options: RenderFigureOptions) -> RenderResult: ...


class FigureRenderer(BaseRenderer):
    def __init__(self, name: str = "", *, theme: Theme | None = None):
        super().__init__(
            name=name or uuid.uuid4(),
            theme=theme or Theme.default(),
        )
        self.chart_renderer = ChartRenderer()

    def _render_figure(self, spec: FigureSpec, *, options: RenderFigureOptions) -> RenderResult:
        with mpl.rc_context(build_rc_params(self.theme)):  # 主体上下文中渲染图片
            # Figure
            figure = self._create_figure(spec)
            # Layout
            gs = self._add_gridspec(figure, spec.layout)
            # Render Charts
            for chart_placement in spec.charts:
                row = chart_placement.row - 1
                col = chart_placement.row - 1
                axes = figure.add_subplot(gs[row : row + chart_placement.row_span, col : col + chart_placement.col_span])
                self.chart_renderer.render(axes, chart_placement.chart, options=options)

        return RenderResult(
            artifact=figure,
            metadata={"renderer": self.name},
        )

    def _create_figure(self, spec: FigureSpec, *, options: RenderFigureOptions) -> Figure:
        fig = plt.figure(**options.build_figure_params())
        if spec.title:
            fig.suptitle(
                spec.title,
                **optional_map_or(
                    options.figure,
                    lambda x: x.build_title_params(),
                    default={},
                ),
            )
        return fig

    def _add_gridspec(self, figure: Figure, layout: FigureGridLayout) -> GridSpec:
        if layout is None:
            raise ValueError("Figure Layout must be resolved before rendering.")

        gridspec_params: dict[str, object] = {}
        if layout.hspace is not None:
            gridspec_params["hspace"] = layout.hspace
        if layout.wspace is not None:
            gridspec_params["wspace"] = layout.wspace

        return figure.add_gridspec(nrows=layout.rows, ncols=layout.cols, **gridspec_params)
