from pydantic import BaseModel, ConfigDict, Field

from athena_charts_matplotlib.styles.figure import MatplotlibFigureOptions
from athena_charts_matplotlib.styles.font import MatplotlibFontOptions
from athena_charts_matplotlib.options.saving import MatplotlibSavingOptions


class BaseOptions(BaseModel):
    model_config = ConfigDict(
        extra="forbid",  # 禁止未知字段
        arbitrary_types_allowed=True,  # 允许自定义对象
        validate_assignment=True,  # 修改字段重新校验
        str_strip_whitespace=True,  # 自动 trim
    )


class MatplotlibPaletteOptions(BaseOptions):
    sequence: list[str] | None = Field(None, description="默认颜色调色板")


class MatplotlibOptions(BaseOptions):
    palette: MatplotlibPaletteOptions | None = Field(None, description="颜色调色板配置")
    font: MatplotlibFontOptions | None = Field(None, description="字体配置")
    figure: MatplotlibFigureOptions | None = Field(None, description="画布配置")
    saving: MatplotlibSavingOptions | None = Field(None, description="保存 Figure 的配置")
