import asyncio

from athena_kit.lark.aclient import AsyncLarkClient


async def main():
    app_id = "cli_a97aa13c63b91cce"
    app_secret = "fWBDioeSjA0vgj9tFAk2NhO2Xii1K7aU"
    async with AsyncLarkClient(app_id, app_secret) as client:
        # spreadsheet, url = await client.sheets.create_spreadsheet("AnS1fzXXCluTEYdIB7FcGNQCnnd")
        # print(spreadsheet)
        # print(url)
        app_token = "OMpvbN8T1aFkkysB57ncuBTpnmb"
        table_id = "tblm5MUWbSAByUsa"
        print(await client.bitables.fields.get_table_fields(app_token, table_id))
        print(await client.bitables.records.get_table_records(app_token, table_id))


if __name__ == "__main__":
    asyncio.run(main())
