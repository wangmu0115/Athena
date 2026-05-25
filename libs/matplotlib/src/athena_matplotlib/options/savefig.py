from typing import Self

from pydantic import Field

from athena_matplotlib.options._base import _BaseOptions
from athena_matplotlib.types import BboxInches, ImageFormat


class PngExportStyle(_BaseOptions):
    compress_level: int = Field(6, ge=0, le=9, description="ZLIB 压缩级别：1=表示速度最快，9=表示压缩率最高，0=表示完全不压缩")
    optimize: bool = Field(False, description="为 True 时会优化 PNG 编码，输出变慢但是文件会变小")


class SaveFigureOptions(_BaseOptions):
    dpi: int | None = Field(None, gt=0, description="输出分辨率")
    format: ImageFormat | None = Field(None, description="输出图片格式")
    facecolor: str | None = Field(None, description="背景颜色")
    edgecolor: str | None = Field(None, description="边框颜色")
    transparent: bool | None = Field(None, description="是否透明背景")
    bbox_inches: BboxInches | None = Field(None, description="图像边界框模式")
    pad_inches: float | None = Field(None, ge=0, description="当 bbox_inches 设置为 `tight` 时，图形周围的内边距，单位 inch")

    png_style: PngExportStyle | None = Field(None, description="当导出为 `png` 格式时，`pil_kwargs` 配置项")

    def build_saving_params(self) -> dict[str, object]:
        params = self.model_dump(exclude_none=True, exclude={"png_style"})

        if self.bbox_inches == "standard":
            params["bbox_inches"] = None

        if self.format in ("png", None) and self.png_style is not None:
            params["pil_kwargs"] = self.png_style.model_dump()

        return params

    @classmethod
    def transparent_png(
        cls,
        dpi: int = 150,
        bbox_inches: BboxInches = "tight",
        pad_inches: float = 0.1,
        pil_compress_level: int = 6,
        pil_optimize: bool = False,
    ) -> Self:
        return cls(
            dpi=dpi,
            format="png",
            facecolor="none",
            edgecolor="none",
            transparent=True,
            bbox_inches=bbox_inches,
            pad_inches=pad_inches,
            png_style=PngExportStyle(compress_level=pil_compress_level, optimize=pil_optimize),
        )

    @classmethod
    def png(
        cls,
        dpi: int = 150,
        facecolor: str = "white",
        edgecolor: str = "white",
        bbox_inches: BboxInches = "tight",
        pad_inches: float = 0.1,
        pil_compress_level: int = 6,
        pil_optimize: bool = False,
    ) -> Self:
        return cls(
            dpi=dpi,
            format="png",
            facecolor=facecolor,
            edgecolor=edgecolor,
            transparent=False,
            bbox_inches=bbox_inches,
            pad_inches=pad_inches,
            png_style=PngExportStyle(compress_level=pil_compress_level, optimize=pil_optimize),
        )
