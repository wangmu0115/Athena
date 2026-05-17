from io import BytesIO
from typing import Literal

from matplotlib.figure import Figure
from pydantic import Field

from athena_core.models import BaseAthenaModel


class MatplotlibFigureArtifact(BaseAthenaModel):
    """Writable Matplotlib Figure artifact.

    This artifact wraps a Matplotlib ``Figure`` object and exposes a unified
    binary export interface through ``to_bytes()``.

    The artifact is designed to integrate with the generic ``WritableArtifact``
    protocol defined in ``athena-charts``.

    Notes:
        - The artifact itself does not manage figure lifecycle.
        - Figure closing should be handled externally by the renderer pipeline or
          artifact finalizer.
        - Export-related options such as DPI and transparency are renderer/runtime
          concerns rather than chart theme concerns.
    """

    figure: Figure | None = Field(..., description="Matplotlib Figure 对象")
    format: Literal["png", "svg", "pdf"] = Field("png", description="文件格式")
    dpi: int = Field(200, gt=0, description="分辨率，每英寸点数")
    bbox_inches: Literal["tight", "standard"] | None = Field(None, description="保存边界")
    transparent: bool = Field(False, description="是否透明背景")

    @property
    def media_type(self) -> str:
        return _MEDIA_TYPES[self.format]

    @property
    def suffix(self) -> str:
        return f".{self.format}"

    def to_bytes(self) -> bytes:
        buffer = BytesIO()
        self.figure.savefig(buffer)
        buffer.seek(0)
        return buffer.getvalue()


_MEDIA_TYPES: dict[str, str] = {
    "png": "image/png",
    "svg": "image/svg+xml",
    "pdf": "application/pdf",
}
