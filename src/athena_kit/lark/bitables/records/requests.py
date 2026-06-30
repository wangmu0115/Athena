from pydantic import Field

from athena_kit.lark._base import _BaseRequestModel


class SearchBitableRecordsRequest(_BaseRequestModel):
    view_id: str | None = Field(default=None, description="多维表格中视图的唯一标识")
    field_names: list[str] | None = Field(default=None, description="本次查询返回记录中包含的字段")
    automatic_fields: bool | None = Field(
        default=None,
        description="是否返回创建时间、修改时间、创建人、修改人等记录元数据",
    )
