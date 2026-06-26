from typing import Any

from athena_kit.lark.bitables.models import BitableField, BitableRecord


def to_bitable_records(raw_records: Any) -> list[BitableRecord]:
    """将飞书响应中的记录列表转换为稳定的公开类型。

    References:
        https://open.feishu.cn/document/server-docs/docs/bitable-v1/bitable-structure
    """
    if not isinstance(raw_records, list):
        raise TypeError("Lark bitable records should be a list.")

    records: list[BitableRecord] = []
    for raw_record in raw_records:
        if not isinstance(raw_record, dict):
            raise TypeError("Each Lark bitable record should be an object.")

        record_id = raw_record.get("record_id")
        fields = raw_record.get("fields")
        if not isinstance(record_id, str) or not isinstance(fields, dict):
            raise TypeError("Each Lark bitable record must contain string `record_id` and object `fields`.")

        record = BitableRecord(record_id=record_id, fields=fields)
        for field_name in ("created_by", "created_time", "last_modified_by", "last_modified_time"):
            if field_name in raw_record:
                record[field_name] = raw_record[field_name]
        records.append(record)

    return records


def to_bitable_fields(raw_fields: Any) -> list[BitableField]:
    """将飞书响应中的字段元数据转换为稳定的公开类型。"""
    if not isinstance(raw_fields, list):
        raise TypeError("Lark bitable fields should be a list.")

    fields: list[BitableField] = []
    for raw_field in raw_fields:
        if not isinstance(raw_field, dict):
            raise TypeError("Each Lark bitable field should be an object.")

        field_id = raw_field.get("field_id")
        field_name = raw_field.get("field_name")
        field_type = raw_field.get("type")
        field_property = raw_field.get("property")
        if not isinstance(field_id, str) or not isinstance(field_name, str) or not isinstance(field_type, int):
            raise TypeError(
                "Each Lark bitable field must contain string `field_id`, string `field_name`, and int `type`."
            )
        if field_property is not None and not isinstance(field_property, dict):
            raise TypeError("Each Lark bitable field `property` must be an object or null.")

        field = BitableField(
            field_id=field_id,
            field_name=field_name,
            type=field_type,
            property=field_property,
        )
        if isinstance(raw_field.get("is_primary"), bool):
            field["is_primary"] = raw_field["is_primary"]
        if isinstance(raw_field.get("ui_type"), str):
            field["ui_type"] = raw_field["ui_type"]
        if "description" in raw_field:
            field["description"] = raw_field["description"]
        fields.append(field)

    return fields
