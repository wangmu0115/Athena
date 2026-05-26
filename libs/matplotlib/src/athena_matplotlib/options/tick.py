from typing import Self

from pydantic import Field

from athena_matplotlib.options._base import _BaseOptions
from athena_matplotlib.types import TickDirection


class TickLineOptions(_BaseOptions):
    visible: bool | None = Field(None, description="是否显示刻度线")
    linecolor: str | None = Field(None, description="刻度线颜色", alias="color")
    linewidth: float | None = Field(None, gt=0, description="主刻度线宽度", alias="width")
    linelength: float | None = Field(None, gt=0, description="主刻度线长度", alias="length")
    direction: TickDirection | None = Field(None, description="刻度线方向")

    @classmethod
    def hide(cls) -> Self:
        return cls(visible=False)

    @classmethod
    def show(
        cls,
        linecolor: str | None = None,
        linewidth: float | None = None,
        linelength: float | None = None,
        direction: TickDirection | None = None,
    ):
        return cls(visible=True, linecolor=linecolor, linewidth=linewidth, linelength=linelength, direction=direction)


class TickLabelOptions(_BaseOptions):
    visible: bool | None = Field(None, description="是否显示刻度文本")
    labelsize: int | None = Field(None, gt=0, description="刻度文本字号")
    labelcolor: str | None = Field(None, description="刻度文本颜色")
    rotation: float | None = Field(None, ge=-90, le=90, description="刻度文本旋转角度")

    @classmethod
    def hide(cls) -> Self:
        return cls(visible=False)

    @classmethod
    def show(
        cls,
        labelsize: int | None = None,
        labelcolor: str | None = None,
        rotation: float | None = None,
    ):
        return cls(visible=True, labelsize=labelsize, labelcolor=labelcolor, rotation=rotation)


class TickOptions(_BaseOptions):
    line: TickLineOptions | None = Field(None, description="刻度线配置项")
    label: TickLabelOptions | None = Field(None, description="刻度文本配置项")

    def build_line_params(self) -> dict[str, object]:
        if self.line is None:
            return {}
        return self.line.model_dump(exclude_none=True, by_alias=True)

    def build_label_params(self) -> dict[str, object]:
        if self.label is None:
            return {}
        return self.label.model_dump(exclude_none=True, by_alias=True)
