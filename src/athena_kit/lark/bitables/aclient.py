import httpx
from athena_kit.lark.bitables.field_client import LarkBitableFieldsAsyncClient
from athena_kit.lark.bitables.record_client import LarkBitableRecordsAsyncClient


class LarkBitablesAsyncClient:
    def __init__(self, aclient: httpx.AsyncClient):
        self.records = LarkBitableRecordsAsyncClient(aclient)
        self.fields = LarkBitableFieldsAsyncClient(aclient)
