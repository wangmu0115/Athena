from collections.abc import Callable

from athena_charts.runtime.context import DefaultPipelineContext, PipelineContextProvider
from athena_charts.runtime.renderers import Renderer, RenderResult, RenderSpec
from athena_charts.runtime.writers import Writer, WriteResult
from athena_charts.themes.base import Theme


class Pipeline[TArtifact, TValue]:
    """渲染输出流水线。Pipeline 本身不关心具体绘图库，也不关心输出目标，只负责流程编排。

    负责串联 Renderer 与 Writer：
        RenderSpec -> RenderResult[TArtifact] -> WriteResult[TValue]
    """

    def __init__(
        self,
        renderer: Renderer[TArtifact],
        writer: Writer[TArtifact, TValue],
        *,
        context_provider: PipelineContextProvider | None = None,
        artifact_finalizer: Callable[[RenderResult[TArtifact]], None] | None = None,
    ):
        self._renderer = renderer
        self._writer = writer
        self._context_provider = context_provider or DefaultPipelineContext()
        self._artifact_finalizer = artifact_finalizer

    def invoke(
        self,
        spec: RenderSpec,
        *,
        filename: str | None = None,
        theme: Theme | None = None,
    ) -> WriteResult[TValue]:
        with self._context_provider.pipeline_context():
            rendered = self._renderer.render(spec, theme=theme)
            try:
                return self._writer.write(rendered, filename=filename)
            finally:
                if self._artifact_finalizer is not None:
                    self._artifact_finalizer(rendered)
