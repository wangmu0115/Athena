from contextlib import AbstractContextManager, nullcontext
from typing import Protocol, runtime_checkable


@runtime_checkable
class PipelineContextProvider(Protocol):
    """渲染上下文"""

    def pipeline_context(self) -> AbstractContextManager[None]: ...


class DefaultPipelineContext:
    def pipeline_context(self) -> AbstractContextManager[None]:
        return nullcontext()
