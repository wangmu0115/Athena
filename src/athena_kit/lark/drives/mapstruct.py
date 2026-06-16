from typing import Any

from athena_kit.core.temporal.codec.temporal import TemporalCodec
from athena_kit.lark.drives.responses import LarkFile, LarkFileType, ShortcutFileInfo


def mapping_files(raw_files: Any) -> list[LarkFile]:
    if not isinstance(raw_files, list):
        return []
    lark_files: list[LarkFile] = []
    temporal_codec = TemporalCodec()
    for raw_file in raw_files:
        if not isinstance(raw_file, dict):
            continue
        lark_file = mapping_file(raw_file, temporal_codec)
        if lark_file:
            lark_files.append(lark_file)
    return lark_files


def mapping_file(raw_file: dict[str, Any], temporal_codec: TemporalCodec | None) -> LarkFile | None:
    if not raw_file:
        return None

    temporal_codec = temporal_codec or TemporalCodec()

    file_type = LarkFileType.from_value(raw_file.get("type", ""))

    lark_file = LarkFile(
        token=raw_file.get("token", ""),
        name=raw_file.get("name", ""),
        type=file_type,
        parent_token=raw_file.get("parent_token", ""),
        url=raw_file.get("url", ""),
        created_time=temporal_codec.parse_datetime(float(raw_file.get("created_time", "")), timestamp_unit="s"),
        modified_time=temporal_codec.parse_datetime(float(raw_file.get("modified_time", "")), timestamp_unit="s"),
    )

    if file_type == LarkFileType.Shortcut:
        raw_shortcut_info = raw_file.get("shortcut_info")
        if not isinstance(raw_shortcut_info, dict):
            return lark_file

        shortcut_info = ShortcutFileInfo(
            target_type=LarkFileType.from_value(raw_shortcut_info.get("target_type", "")),
            target_token=raw_shortcut_info.get("target_token", ""),
        )
        lark_file["shortcut_info"] = shortcut_info

    return lark_file
