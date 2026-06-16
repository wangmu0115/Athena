import asyncio
import logging

from athena_kit.http.hooks.logging import LoggingOptions
from athena_kit.lark.aclient import AsyncLarkClient


async def main():
    app_id = "cli_a97aa13c63b91cce"
    app_secret = "fWBDioeSjA0vgj9tFAk2NhO2Xii1K7aU"
    async with AsyncLarkClient(app_id, app_secret, logging=LoggingOptions(level=logging.WARNING)) as client:
        folder_token = "EmbrfoG9MlJC9YdTOuucPLmjnHg"
        print(await client.drives.list_files(folder_token))


if __name__ == "__main__":
    asyncio.run(main())
