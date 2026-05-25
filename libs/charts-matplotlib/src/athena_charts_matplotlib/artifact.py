from io import BytesIO

from matplotlib.figure import Figure

from athena_charts_matplotlib.rendering.options import SaveFigureOptions
from athena_core.values.optional import optional_map_or, optional_or, safe_getattr

_MEDIA_TYPES: dict[str, str] = {
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "svg": "image/svg+xml",
    "pdf": "application/pdf",
    "eps": "application/postscript",
    "ps": "application/postscript",
    "webp": "image/webp",
}


class MatplotlibFigureArtifact:
    """Writable Matplotlib `Figure` artifact.

    The artifact is designed to integrate with the generic `WritableArtifact` protocol.

    Notes:
        - The artifact itself does not manage figure lifecycle.
        - Figure closing should be handled externally by the renderer pipeline or artifact finalizer.
    """

    def __init__(self, figure: Figure, *, options: SaveFigureOptions | None = None):
        self._figure = figure
        self._options = options
        self._format = optional_or(safe_getattr(options, "format"), default="png")

    @property
    def media_type(self) -> str:
        return _MEDIA_TYPES[self._format]

    @property
    def suffix(self) -> str:
        return f".{self._format}"

    def to_bytes(self) -> bytes:
        buffer = BytesIO()
        params = optional_map_or(
            self._options,
            lambda x: x.build_saving_params(),
            default={},
        )
        self._figure.savefig(
            buffer,
            **params,
        )
        buffer.seek(0)
        return buffer.getvalue()

    def close(self) -> None:
        import matplotlib.pyplot as plt

        plt.close(self._figure)
