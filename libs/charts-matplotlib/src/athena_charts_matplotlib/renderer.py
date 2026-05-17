import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from athena_charts.runtime import BaseRenderer, RenderResult
from athena_charts.specs.figures import FigureSpec
from athena_charts.themes import Theme
from athena_charts_matplotlib.artifact import MatplotlibFigureArtifact
from athena_charts_matplotlib.options.base import MatplotlibOptions
from athena_charts_matplotlib.themes.context import matplotlib_theme_context


class MatplotlibRenderer(BaseRenderer[MatplotlibFigureArtifact]):
    def __init__(
        self,
        name: str = "",
        theme: Theme | None = None,
        *,
        options: MatplotlibOptions | None = None,
    ):
        super().__init__(name=name, theme=theme)
        self._options = options or MatplotlibOptions()

    def _render_figure(self, spec: FigureSpec) -> MatplotlibFigureArtifact:
        with matplotlib_theme_context(self.theme, self._options):
            fig = self._create_figure()

        layout = spec.layout
        if layout is None or layout.rows is None or layout.cols is None:
            raise ValueError("Figure layout must be resolved before rendering.")

        plt.figure()

        options = spec.options

    def _create_figure(self) -> Figure:
        pass

    # labels: FigureLabels = Field(default_factory=FigureLabels, description="画布级文本标签")
    # charts: list[ChartPlacement] = Field(default_factory=list, description="画布中的图表放置列表")
    # options: FigureOptions = Field(default_factory=FigureOptions, description="画布级渲染选项")


def close_matplotlib_figure_artifact(result: RenderResult[MatplotlibFigureArtifact]) -> None:
    plt.close(result.artifact.figure)
