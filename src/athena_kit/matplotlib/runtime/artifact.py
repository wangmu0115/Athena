from io import BytesIO
from typing import Protocol, runtime_checkable

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from athena_kit.core.values.optional import optional_or
from athena_kit.matplotlib.options import SaveFigureOptions
from athena_kit.matplotlib.types import ImageFormat

_MEDIA_TYPES: dict[ImageFormat, str] = {
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "svg": "image/svg+xml",
    "pdf": "application/pdf",
    "eps": "application/postscript",
    "ps": "application/postscript",
    "webp": "image/webp",
}


@runtime_checkable
class WritableArtifact(Protocol):
    media_type: str
    suffix: str

    def to_bytes(self) -> bytes:
        """转换为二进制内容"""
        ...

    def close(self) -> None: ...


class FigureArtifact:
    """Writable Matplotlib `Figure` artifact."""

    def __init__(self, figure: Figure, *, options: SaveFigureOptions | None = None):
        self._figure = figure
        self._options = options or SaveFigureOptions.png()
        self._format = optional_or(self._options.format, default="png")

    @property
    def media_type(self) -> str:
        return _MEDIA_TYPES[self._format]

    @property
    def suffix(self) -> str:
        return f".{self._format}"

    def to_bytes(self) -> bytes:
        buffer = BytesIO()

        params = self._options.build_saving_params()
        self._figure.savefig(buffer, **params)
        buffer.seek(0)

        return buffer.getvalue()

    def close(self) -> None:

        plt.close(self._figure)
