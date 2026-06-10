from pydantic import BaseModel, Field


class LarkSheetLocatorConfig(BaseModel):
    spreadsheet_token: str = Field(..., description="Lark spreadsheet token")
    sheet_id: str = Field(..., description="Lark sheet ID")


class LarkConfig(BaseModel):
    app_id: str = Field(..., description="Lark app ID")
    app_secret: str = Field(..., description="Lark app secret")
    api_base_url: str = Field("https://open.feishu.cn/open-apis", description="Lark Open API base URL")
