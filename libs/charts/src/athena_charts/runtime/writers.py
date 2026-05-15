from abc import ABC, abstractmethod
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Protocol, runtime_checkable
from uuid import uuid4

from pydantic import Field

from athena_charts.runtime.renderers import RenderResult, WritableArtifact
from athena_core.models import BaseAthenaModel


class WriteResult[TValue](BaseAthenaModel):
    value: TValue = Field(..., description="输出值，例如路径、Bytes、URL、对象存储 Key 等")
    media_type: str = Field(..., description="输出媒体类型")
    filename: str | None = Field(None, description="文件名")
    metadata: dict[str, object] = Field(default_factory=dict, description="元数据信息")


@runtime_checkable
class Writer[TValue](Protocol):
    """输出器"""

    def write(self, rendered: RenderResult, *, filename: str | None = None) -> WriteResult[TValue]: ...


class BaseWriter[TValue](ABC):
    def write(self, rendered: RenderResult, *, filename: str | None = None) -> WriteResult[TValue]:
        artifact = rendered.artifact

        if not isinstance(rendered.artifact, WritableArtifact):
            raise TypeError(f"{type(artifact).__name__} does not implement WritableArtifact.")

        return self._write_artifact(artifact, filename=filename)

    @abstractmethod
    def _write_artifact(self, artifact: WritableArtifact, *, filename: str | None = None) -> WriteResult[TValue]: ...


class FileWriter(BaseWriter[Path]):
    """写出到本地目录"""

    def __init__(self, directory: str | Path):
        self._directory = Path(directory)

    def _write_artifact(self, artifact: WritableArtifact, *, filename: str | None = None) -> WriteResult[Path]:
        self._directory.mkdir(parents=True, exist_ok=True)

        final_name = ensure_filename(filename, suffix=artifact.suffix)
        path = self._directory / final_name
        path.write_bytes(artifact.to_bytes())

        return WriteResult(
            value=path,
            media_type=artifact.media_type,
            filename=final_name,
        )


class TempFileWriter(BaseWriter[Path]):
    """写出到临时文件"""

    def _write_artifact(self, artifact: WritableArtifact, *, filename: str | None = None) -> WriteResult[Path]:
        final_name = ensure_filename(filename, suffix=artifact.suffix)

        with NamedTemporaryFile(delete=False, suffix=artifact.suffix) as file:
            file.write_bytes(artifact.to_bytes())
            path = Path(file.name)

            return WriteResult(
                value=path,
                media_type=artifact.media_type,
                filename=final_name,
                metadata={"temporary": True},
            )


class MemoryWriter:
    """写出到内存。"""

    def _write_artifact(self, artifact: WritableArtifact, *, filename: str | None = None) -> WriteResult[bytes]:
        final_name = ensure_filename(filename, suffix=artifact.suffix)

        return WriteResult(
            value=artifact.to_bytes(),
            media_type=artifact.media_type,
            filename=final_name,
        )


def ensure_filename(filename: str | None, *, suffix: str) -> str:
    if filename:
        return filename if filename.endswith(suffix) else f"{filename}{suffix}"
    return f"{uuid4().hex}{suffix}"
