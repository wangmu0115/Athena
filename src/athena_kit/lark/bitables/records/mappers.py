from datetime import UTC, datetime
from typing import Any

from athena_kit.lark.bitables.models import BitableRecord


def _from_millisecond_timestamp(timestamp: Any, *, field_name: str) -> datetime:
    if not isinstance(timestamp, int):
        raise TypeError(f"Lark bitable record `{field_name}` must be an int millisecond timestamp.")
    return datetime.fromtimestamp(timestamp / 1000, tz=UTC)


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
        if "created_by" in raw_record:
            created_by = raw_record["created_by"]
            if not isinstance(created_by, dict):
                raise TypeError("Lark bitable record `created_by` must be an object.")
            record["created_by"] = created_by
        if "created_time" in raw_record:
            record["created_time"] = _from_millisecond_timestamp(
                raw_record["created_time"],
                field_name="created_time",
            )
        if "last_modified_by" in raw_record:
            last_modified_by = raw_record["last_modified_by"]
            if not isinstance(last_modified_by, dict):
                raise TypeError("Lark bitable record `last_modified_by` must be an object.")
            record["last_modified_by"] = last_modified_by
        if "last_modified_time" in raw_record:
            record["last_modified_time"] = _from_millisecond_timestamp(
                raw_record["last_modified_time"],
                field_name="last_modified_time",
            )
        records.append(record)

    return records
