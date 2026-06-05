import matplotlib as mpl
import matplotlib.pyplot as plt

from athena_kit.matplotlib.options import RenderFigureOptions, SaveFigureOptions
from athena_kit.matplotlib.runtime.context import build_rc_params
from athena_kit.matplotlib.runtime.renderer import BaseRenderer, FigureRenderer, RenderSpec
from athena_kit.matplotlib.runtime.writers import BaseWriter, TempFileWriter, WriteResult
from athena_kit.matplotlib.styles import Theme


class Pipeline[TValue]:
    """渲染输出流水线，负责串联 Renderer 与 Writer。"""

    def __init__(
        self,
        renderer: BaseRenderer | None,
        writer: BaseWriter[TValue] | None,
        *,
        theme: Theme | None = None,
    ):
        self._theme = theme or Theme.default()
        self._renderer = renderer or FigureRenderer(name="", theme=self._theme)
        self._writer = writer or TempFileWriter()

    def invoke(
        self,
        spec: RenderSpec,
        *,
        filename: str | None = None,
        render_options: RenderFigureOptions | None = None,
        save_options: SaveFigureOptions | None = None,
    ) -> WriteResult[TValue]:
        with mpl.rc_context(build_rc_params(self._theme)):
            render_result = self._renderer.render(spec, options=render_options)
            try:
                write_result = self._writer.write(render_result.figure, filename=filename, options=save_options)
                write_result.metadata.update(render_result.metadata)  # 更新 Render metadata
                return write_result
            finally:
                plt.close(render_result.figure)
