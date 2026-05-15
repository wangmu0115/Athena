from typing import Protocol, runtime_checkable

from pydantic import Field

from athena_charts.runtime.renderers import RenderResult
from athena_core.models import BaseAthenaModel


class WriteResult[TValue](BaseAthenaModel):
    value: TValue = Field(..., description="输出值，例如路径、Bytes、URL、对象存储 Key 等")
    media_type: str = Field(..., description="输出媒体类型")
    filename: str | None = Field(None, description="文件名")
    metadata: dict[str, object] = Field(default_factory=dict, description="元数据信息")


@runtime_checkable
class Writer[TArtifact, TValue](Protocol):
    """输出器"""

    def write(self, rendered: RenderResult[TArtifact], *, filename: str | None = None) -> WriteResult[TValue]: ...
