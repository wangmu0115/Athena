import asyncio

from athena_kit.lark.aclient import AsyncLarkClient


async def main():
    app_id = "cli_a97aa13c63b91cce"
    app_secret = "fWBDioeSjA0vgj9tFAk2NhO2Xii1K7aU"
    async with AsyncLarkClient(app_id, app_secret) as client:
        # spreadsheet, url = await client.sheets.create_spreadsheet("AnS1fzXXCluTEYdIB7FcGNQCnnd")
        # print(spreadsheet)
        # print(url)
        spreadsheet_token = "IukqsB3vThljQgt8JYicoyM5nUg"
        print(await client.sheets.batch_add_sheets(spreadsheet_token, ["a", "b", "c"]))


if __name__ == "__main__":
    asyncio.run(main())
