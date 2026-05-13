from pydantic import BaseModel, ConfigDict


class BaseAthenaModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",                # 禁止未知字段
        arbitrary_types_allowed=True,  # 允许自定义对象
        populate_by_name=True,         # alias 与 field_name 双支持
        validate_assignment=False,     # 修改字段不重新校验
        str_strip_whitespace=True,     # 自动 trim
    )  # fmt: off
