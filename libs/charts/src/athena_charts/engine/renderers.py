from abc import abstractmethod
from typing import Protocol, runtime_checkable

from pydantic import Field

from athena_charts.charts.chart import ChartSpec
from athena_charts.figure import FigureSpec
from athena_charts.themes import Theme
from athena_charts.themes.base import DEFAULT_THEME
from athena_core.models.base import BaseAthenaModel

type RenderSpec = ChartSpec | FigureSpec


class RenderResult[TArtifact](BaseAthenaModel):
    artifact: TArtifact = Field(..., description="渲染结果产物")
    metadata: dict[str, object] = Field(default_factory=dict, description="元数据信息")


@runtime_checkable
class Renderer[TArtifact](Protocol):
    """绘图渲染器"""

    def render(self, spec: RenderSpec, *, theme: Theme | None = None) -> RenderResult[TArtifact]: ...


class BaseRenderer[TArtifact]:
    def __init__(self, name: str = "", theme: Theme | None = None):
        self._name = name  # tracing
        self._theme = theme or DEFAULT_THEME

    @property
    def theme(self) -> Theme:
        return self._theme

    def render(self, spec: RenderSpec, *, theme: Theme | None = None) -> RenderResult[TArtifact]:
        figure_spec = FigureSpec.from_chart(spec) if isinstance(spec, ChartSpec) else spec
        return self._render_figure(
            figure_spec,
            theme=theme or self._theme,
        )

    @abstractmethod
    def _render_figure(self, spec: FigureSpec, *, theme: Theme) -> RenderResult[TArtifact]: ...
