from typing import TYPE_CHECKING

from athena_core._import_utils import import_attr

if TYPE_CHECKING:
    from athena_charts.runtime.context import DefaultPipelineContext, PipelineContextProvider
    from athena_charts.runtime.pipeline import Pipeline
    from athena_charts.runtime.renderers import Renderer, RenderResult, RenderSpec
    from athena_charts.runtime.writers import Writer, WriteResult


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
    "Writer": "writers",
    "WriteResult": "writers",
    "Pipeline": "pipeline",
    "Renderer": "renderers",
    "RenderResult": "renderers",
    "RenderSpec": "renderers",
    "DefaultPipelineContext": "context",
    "PipelineContextProvider": "context",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    result = import_attr(attr_name, module_name, __spec__.parent)
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)
