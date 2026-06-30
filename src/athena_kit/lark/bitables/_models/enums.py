from athena_kit.core.models import LabelIntEnum, LabelStrEnum


class BitableFieldType(LabelIntEnum):
    """多维表格字段类型。

    References:
        https://open.feishu.cn/document/server-docs/docs/bitable-v1/app-table-field/guide#46001acf
    """

    TEXT = 1, "文本", "Text", "Barcode", "Email"
    NUMBER = 2, "数字", "Number", "Progress", "Currency", "Rating"
    SINGLE_SELECT = 3, "单选", "SingleSelect"
    MULTI_SELECT = 4, "多选", "MultiSelect"
    DATE_TIME = 5, "日期", "DateTime"
    CHECKBOX = 7, "复选框", "Checkbox"
    USER = 11, "人员", "User"
    PHONE = 13, "电话号码", "Phone"
    URL = 15, "超链接", "Url"
    ATTACHMENT = 17, "附件", "Attachment"
    SINGLE_LINK = 18, "关联", "SingleLink"
    LOOKUP = 19, "查找引用", "Lookup"
    FORMULA = 20, "公式", "Formula"
    DUPLEX_LINK = 21, "双向关联", "DuplexLink"
    LOCATION = 22, "地理位置", "Location"
    GROUP_CHAT = 23, "群组", "GroupChat"
    STAGE = 24, "流程", "Stage"
    CREATED_TIME = 1001, "创建时间", "CreatedTime"
    MODIFIED_TIME = 1002, "最后更新时间", "ModifiedTime"
    CREATED_USER = 1003, "创建人", "CreatedUser"
    MODIFIED_USER = 1004, "修改人", "ModifiedUser"
    AUTO_NUMBER = 1005, "自动编号", "AutoNumber"
    BUTTON = 3001, "按钮", "Button"


class BitableFieldUiType(LabelStrEnum):
    """多维表格字段在界面上的展示类型。

    References:
        https://open.feishu.cn/document/server-docs/docs/bitable-v1/app-table-field/guide#46001acf
    """

    TEXT = "Text", "文本"
    EMAIL = "Email", "邮箱"
    BARCODE = "Barcode", "条码"
    NUMBER = "Number", "数字"
    PROGRESS = "Progress", "进度"
    CURRENCY = "Currency", "货币"
    RATING = "Rating", "评分"
    SINGLE_SELECT = "SingleSelect", "单选"
    MULTI_SELECT = "MultiSelect", "多选"
    DATE_TIME = "DateTime", "日期"
    CHECKBOX = "Checkbox", "复选框"
    USER = "User", "人员"
    GROUP_CHAT = "GroupChat", "群组"
    STAGE = "Stage", "流程"
    PHONE = "Phone", "电话号码"
    URL = "Url", "超链接"
    ATTACHMENT = "Attachment", "附件"
    SINGLE_LINK = "SingleLink", "单向关联"
    FORMULA = "Formula", "公式"
    LOOKUP = "Lookup", "查找引用"
    DUPLEX_LINK = "DuplexLink", "双向关联"
    LOCATION = "Location", "地理位置"
    CREATED_TIME = "CreatedTime", "创建时间"
    MODIFIED_TIME = "ModifiedTime", "最后更新时间"
    CREATED_USER = "CreatedUser", "创建人"
    MODIFIED_USER = "ModifiedUser", "修改人"
    AUTO_NUMBER = "AutoNumber", "自动编号"
    BUTTON = "Button", "按钮"
