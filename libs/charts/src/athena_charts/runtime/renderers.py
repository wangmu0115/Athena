from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable

from pydantic import Field

from athena_charts.specs.charts import ChartSpec
from athena_charts.specs.figures import FigureSpec
from athena_core.models import BaseAthenaModel

type RenderSpec = ChartSpec | FigureSpec


class RenderResult[TArtifact](BaseAthenaModel):
    artifact: TArtifact = Field(..., description="渲染结果")
    metadata: dict[str, object] = Field(default_factory=dict, description="元数据信息")


@runtime_checkable
class Renderer[TArtifact](Protocol):
    """Renderer Protocol

    渲染器最小协议：接收 RenderSpec 并返回 RenderResult
    """

    @property
    def name(self) -> str: ...

    def render(self, spec: RenderSpec) -> RenderResult[TArtifact]: ...


class BaseRenderer[TArtifact](ABC):
    def __init__(self, name: str = ""):
        self._name = name  # tracing

    @property
    def name(self) -> str:
        return self._name

    def render(self, spec: RenderSpec) -> RenderResult[TArtifact]:
        figure_spec = FigureSpec.from_chart(spec) if isinstance(spec, ChartSpec) else spec
        return self._render_figure(figure_spec)

    @abstractmethod
    def _render_figure(self, spec: FigureSpec) -> RenderResult[TArtifact]: ...
