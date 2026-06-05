from pydantic import BaseModel, ConfigDict, Field

from athena_kit.matplotlib.types import FontFamily, FontWeight


class _BaseStyle(BaseModel):
    model_config = ConfigDict(
        extra="forbid",  # 禁止未知字段
        arbitrary_types_allowed=True,  # 允许自定义对象
        str_strip_whitespace=True,  # 自动 trim
    )


class FontStyle(_BaseStyle):
    family: FontFamily | None = Field(None, description="默认字体族")
    fallbacks: list[str] | None = Field(None, description="字体列表")
    size: int | None = Field(None, gt=0, description="默认字号")
    weight: FontWeight | None = Field(None, description="默认字体粗细")
    color: str | None = Field(None, description="默认文本颜色")


class PaletteStyle(_BaseStyle):
    colors: list[str] | None = Field(None, description="默认颜色循环列表，按图层或序列顺序依次取色")
