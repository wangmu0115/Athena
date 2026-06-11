"""A1 notation helpers for Lark Sheets ranges.

References:
    https://developers.google.com/sheets/api/guides/concepts#cell
    https://support.microsoft.com/office/switch-between-relative-absolute-and-mixed-references-dfec08cd-ae65-4f56-839e-5f0d8d0baca9
    https://open.feishu.cn/document/server-docs/docs/sheets-v3/overview#9049d332
"""


def column_name_to_index(column_name: str) -> int:
    """将 A1 notation 中的列名转换为从 1 开始的列序号。

    示例：
        - `"A"` -> `1`
        - `"Z"` -> `26`
        - `"AA"` -> `27`

    References:
        https://developers.google.com/sheets/api/guides/concepts#cell
    """
    column_name = column_name.upper()
    index = 0
    for i, char in enumerate(reversed(column_name)):
        index += (ord(char) - ord("A") + 1) * (26**i)
    return index


def column_index_to_name(index: int) -> str:
    """将从 1 开始的列序号转换为 A1 notation 中的列名。

    示例：
        - `1` -> `"A"`
        - `26` -> `"Z"`
        - `27` -> `"AA"`

    References:
        https://developers.google.com/sheets/api/guides/concepts#cell
    """
    column_name = ""
    while index > 0:
        index -= 1
        column_name = chr((index % 26) + ord("A")) + column_name
        index //= 26
    return column_name


def build_a1_range(
    sheet_id: str,
    n_rows: int,
    n_cols: int,
    start_row: int = 1,
    start_col: int = 1,
) -> str:
    """构造飞书表格 API 使用的 A1 notation 范围字符串。

    返回格式为 `{sheet_id}!{start_col}{start_row}:{end_col}{end_row}`，例如 `"sheet1!A1:D5"`。
    行号和列号均从 1 开始计数。

    References:
        https://open.feishu.cn/document/server-docs/docs/sheets-v3/data-operation/write-data-to-a-single-range
        https://open.feishu.cn/document/server-docs/docs/sheets-v3/data-operation/reading-a-single-range
        https://developers.google.com/sheets/api/guides/concepts#cell
    """
    end_col = column_index_to_name(start_col + n_cols - 1)
    end_row = start_row + n_rows - 1
    return f"{sheet_id}!{column_index_to_name(start_col)}{start_row}:{end_col}{end_row}"
