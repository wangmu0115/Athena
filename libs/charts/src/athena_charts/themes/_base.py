from pydantic import BaseModel, ConfigDict


class _BaseTheme(BaseModel):
    model_config = ConfigDict(
        extra="forbid",  # 禁止未知字段
        arbitrary_types_allowed=True,  # 允许自定义对象
        str_strip_whitespace=True,  # 自动 trim
    )
