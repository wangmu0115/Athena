from datetime import datetime
from typing import NotRequired, TypedDict

from athena_kit.core.models.enums import LabelStrEnum


class LarkFileType(LabelStrEnum):
    Doc = ("doc", "旧版文档")
    Docx = ("docx", "新版文档")
    Sheet = ("sheet", "表格")
    Bitable = ("bitable", "多维表格")
    Mindnote = ("mindnote", "思维导图")
    File = ("file", "文件")
    Folder = ("folder", "文件夹")
    Shortcut = ("shortcut", "快捷方式")


class ShortcutFileInfo(TypedDict):
    """快捷方式类型文件指向的原文件信息。

    Attributes:
        target_type: 快捷方式指向的原文件类型。
        target_token: 快捷方式指向的原文件 token。
    """

    target_type: LarkFileType
    target_token: str


class LarkFile(TypedDict):
    """文件夹清单中的文件信息。

    Attributes:
        token: 文件标识。
        name: 文件名。
        type: 文件类型。
        parent_token: 父文件夹标识。
        url: 文件在浏览器中的 URL 链接。
        shortcut_info: 快捷方式类型文件的信息，仅当文件类型为 shortcut 时返回。
        created_time: 文件创建时间。
        modified_time: 文件最近修改时间。
    """

    token: str
    name: str
    type: LarkFileType
    parent_token: str
    url: str
    shortcut_info: NotRequired[ShortcutFileInfo]
    created_time: datetime
    modified_time: datetime
