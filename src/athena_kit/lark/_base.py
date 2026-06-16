from typing import Any

from pydantic import BaseModel, ConfigDict


class _BaseRequestModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",  # 禁止未知字段
        arbitrary_types_allowed=True,  # 允许自定义对象
        populate_by_name=True,  # alias 与 field_name 双支持
        validate_assignment=True,  # 修改字段重新校验
        str_strip_whitespace=True,  # 自动 trim
    )

    def to_dict(self, exclude_none: bool = True) -> dict[str, Any]:
        return self.model_dump(
            by_alias=True,
            exclude_none=exclude_none,
        )
