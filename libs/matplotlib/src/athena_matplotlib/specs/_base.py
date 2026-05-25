from pydantic import BaseModel, ConfigDict


class _BaseSpec(BaseModel):
    """声明式图表规范基类，该类仅供 `athena_matplotlib.specs` 内部复用，不作为稳定公共 API 导出。"""

    model_config = ConfigDict(
        extra="forbid",                # 禁止未知字段
        arbitrary_types_allowed=True,  # 允许自定义对象
        validate_assignment=True,      # 修改字段重新校验
        str_strip_whitespace=True,     # 自动 trim
    )  # fmt: off
