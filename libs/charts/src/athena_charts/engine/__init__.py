from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_charts.engine.outputs import Writer, WriteResult
    from athena_charts.engine.pipeline import Pipeline
    from athena_charts.engine.renderers import Renderer, RenderResult, RenderSpec
    from athena_charts.engine.runtime import DefaultPipelineContext, PipelineContextProvider


__all__ = (
    "Writer",
    "WriteResult",
    "Pipeline",
    "Renderer",
    "RenderResult",
    "RenderSpec",
    "DefaultPipelineContext",
    "PipelineContextProvider",
)


_dynamic_imports = {
    "Writer": "outputs",
    "WriteResult": "outputs",
    "Pipeline": "pipeline",
    "Renderer": "renderers",
    "RenderResult": "renderers",
    "RenderSpec": "renderers",
    "DefaultPipelineContext": "runtime",
    "PipelineContextProvider": "runtime",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
