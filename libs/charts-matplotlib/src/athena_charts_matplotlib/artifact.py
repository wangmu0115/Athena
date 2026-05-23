from io import BytesIO

import matplotlib as mpl
from matplotlib.figure import Figure

from athena_charts_matplotlib.options.savefig import MatplotlibSavingOptions
from athena_core.values.optional import optional_map, optional_or, optional_or_else

_MEDIA_TYPES: dict[str, str] = {
    "png": "image/png",
    "svg": "image/svg+xml",
    "pdf": "application/pdf",
}


class MatplotlibFigureArtifact:
    """Writable Matplotlib `Figure` artifact.

    The artifact is designed to integrate with the generic `WritableArtifact` protocol.

    Notes:
        - The artifact itself does not manage figure lifecycle.
        - Figure closing should be handled externally by the renderer pipeline or artifact finalizer.
    """

    def __init__(self, figure: Figure, *, options: MatplotlibSavingOptions | None = None):
        self._figure = figure
        self._options = options
        self._format = optional_or(optional_map(options, lambda x: x.format), default="png")

    @property
    def media_type(self) -> str:
        return _MEDIA_TYPES[self._format]

    @property
    def suffix(self) -> str:
        return f".{self._format}"

    def to_bytes(self) -> bytes:
        buffer = BytesIO()
        self.figure.savefig(buffer, **self._build_saving_params())
        buffer.seek(0)
        return buffer.getvalue()

    def close(self) -> None:
        import matplotlib.pyplot as plt

        plt.close(self._figure)

    def _build_saving_params(self) -> dict[str, object]:
        saving_params: dict[str, object] = {}
        saving_params["format"] = self._format
        dpi = optional_or_else(optional_map(self._options, lambda x: x.dpi), lambda: mpl.rcParams["figure.dpi"])
        saving_params["dpi"] = dpi
        transparent = optional_map(self._options, lambda x: x.transparent)
        if transparent is not None:
            saving_params["transparent"] = transparent
        bbox_inches = optional_map(self._options, lambda x: x.bbox_inches)
        if bbox_inches is not None:
            saving_params["bbox_inches"] = bbox_inches
        pad_inches = optional_map(self._options, lambda x: x.pad_inches)
        if pad_inches is not None:
            saving_params["pad_inches"] = pad_inches

        return saving_params
