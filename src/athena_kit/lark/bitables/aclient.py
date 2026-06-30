import httpx
from athena_kit.lark.bitables.fields import LarkBitableFieldsAsyncClient
from athena_kit.lark.bitables.records import LarkBitableRecordsAsyncClient


class LarkBitablesAsyncClient:
    def __init__(self, aclient: httpx.AsyncClient):
        self.records = LarkBitableRecordsAsyncClient(aclient)
        self.fields = LarkBitableFieldsAsyncClient(aclient)
