from typing import Any

from athena_kit.lark.bitables.models import BitableField, BitableFieldType, BitableFieldUiType


def to_bitable_fields(raw_fields: Any) -> list[BitableField]:
    if not isinstance(raw_fields, list):
        raise TypeError("Lark bitable fields should be a list.")

    fields: list[BitableField] = []
    for raw_field in raw_fields:
        if not isinstance(raw_field, dict):
            raise TypeError("Each Lark bitable field should be an object.")

        field_id = raw_field.get("field_id")
        field_name = raw_field.get("field_name")
        field_type = raw_field.get("type")
        field_ui_type = raw_field.get("ui_type")
        field_property = raw_field.get("property")
        if (
            not isinstance(field_id, str)
            or not isinstance(field_name, str)
            or not isinstance(field_type, int)
            or not isinstance(field_ui_type, str)
        ):
            raise TypeError(
                "Each Lark bitable field must contain string `field_id`, string `field_name`, int `type`, "
                "and string `ui_type`."
            )
        if field_property is not None and not isinstance(field_property, dict):
            raise TypeError("Each Lark bitable field `property` must be an object or null.")

        field = BitableField(
            field_id=field_id,
            field_name=field_name,
            type=_to_bitable_field_type(field_type),
            property=field_property,
            is_primary=raw_field.get("is_primary") is True,
            is_hidden=raw_field.get("is_hidden") is True,
            ui_type=_to_bitable_field_ui_type(field_ui_type),
        )
        if "description" in raw_field:
            field["description"] = raw_field["description"]
        fields.append(field)

    return fields


def _to_bitable_field_type(field_type: int) -> BitableFieldType | int:
    res = BitableFieldType.safe_from_value(field_type)

    return res if res is not None else field_type


def _to_bitable_field_ui_type(field_ui_type: str) -> BitableFieldUiType | str:
    res = BitableFieldUiType.safe_from_value(field_ui_type)

    return res if res is not None else field_ui_type
