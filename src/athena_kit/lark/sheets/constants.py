CREATE_SPREADSHEET_API_URL = "/sheets/v3/spreadsheets"


def OPERATE_SHEET_API_URL(spreadsheet_token: str) -> str:
    return f"/sheets/v2/spreadsheets/{spreadsheet_token}/sheets_batch_update"


def WRITE_SINGLE_RANGE_API_URL(spreadsheet_token: str) -> str:
    return f"/sheets/v2/spreadsheets/{spreadsheet_token}/values"


def READ_SINGLE_RANGE_API_URL(spreadsheet_token: str, range: str) -> str:
    return f"/sheets/v2/spreadsheets/{spreadsheet_token}/values/{range}"
