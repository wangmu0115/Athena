import asyncio

from athena_kit.lark.aclient import AsyncLarkClient


async def main():
    app_id = "cli_a97aa13c63b91cce"
    app_secret = "fWBDioeSjA0vgj9tFAk2NhO2Xii1K7aU"
    async with AsyncLarkClient(app_id, app_secret) as client:
        # spreadsheet, url = await client.sheets.create_spreadsheet("AnS1fzXXCluTEYdIB7FcGNQCnnd")
        # print(spreadsheet)
        # print(url)
        app_token = "HoE7btqu4aXXpfsRpXEc9NFqnzb"
        table_id = "tblYe4Ljda0mhCMt"
        print(await client.bitables.search_records(app_token, table_id, page_size=3))


if __name__ == "__main__":
    asyncio.run(main())
