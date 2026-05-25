import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from tempfile import NamedTemporaryFile

from matplotlib.figure import Figure

from athena_matplotlib.options import SaveFigureOptions
from athena_matplotlib.runtime.artifact import FigureArtifact, WritableArtifact


@dataclass
class WriteResult[TValue]:
    value: TValue
    """输出值，例如路径、Bytes、URL、对象存储 Key 等"""
    media_type: str
    """输出媒体类型"""
    filename: str | None = None
    """文件名"""
    metadata: dict[str, object] = field(default_factory=dict)
    """元数据信息"""


class BaseWriter[TValue](ABC):
    def write(self, figure: Figure, *, filename: str | None = None, options: SaveFigureOptions | None) -> WriteResult[TValue]:
        artifact = FigureArtifact(figure, options=options)

        return self._write_artifact(artifact, filename=filename)

    @abstractmethod
    def _write_artifact(self, artifact: WritableArtifact, *, filename: str | None = None) -> WriteResult[TValue]: ...


class FileWriter(BaseWriter[Path]):
    """写出到本地目录"""

    def __init__(self, directory: str | Path):
        self._directory = Path(directory)

    def _write_artifact(self, artifact: WritableArtifact, *, filename: str | None = None) -> WriteResult[Path]:
        self._directory.mkdir(parents=True, exist_ok=True)

        final_filename = _ensure_filename(filename, suffix=artifact.suffix)
        path = self._directory / final_filename
        path.write_bytes(artifact.to_bytes())

        return WriteResult(
            value=path,
            media_type=artifact.media_type,
            filename=final_filename,
        )


class TempFileWriter(BaseWriter[Path]):
    """写出到临时文件"""

    def _write_artifact(self, artifact: WritableArtifact, *, filename: str | None = None) -> WriteResult[Path]:
        final_filename = _ensure_filename(filename, suffix=artifact.suffix)

        with NamedTemporaryFile(delete=False, suffix=artifact.suffix) as file:
            file.write(artifact.to_bytes())
            path = Path(file.name)

            return WriteResult(
                value=path,
                media_type=artifact.media_type,
                filename=final_filename,
                metadata={"temporary": True},
            )


class MemoryWriter(BaseWriter[bytes]):
    """写出到内存。"""

    def _write_artifact(self, artifact: WritableArtifact, *, filename: str | None = None) -> WriteResult[bytes]:
        final_filename = _ensure_filename(filename, suffix=artifact.suffix)

        return WriteResult(
            value=artifact.to_bytes(),
            media_type=artifact.media_type,
            filename=final_filename,
        )


def _ensure_filename(filename: str | None, *, suffix: str) -> str:
    suffix = suffix if suffix.startswith(".") else f".{suffix}"
    if filename:
        return filename if filename.endswith(suffix) else f"{filename}{suffix}"
    return f"{uuid.uuid4().hex}{suffix}"
