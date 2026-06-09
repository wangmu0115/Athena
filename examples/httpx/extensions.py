# client = httpx.Client()
# response = client.get("https://www.example.com")
# print(response.extensions["http_version"])  # b"HTTP/1.1"
# def log(event_name, info):
#     print(event_name, info)
# client = httpx.Client()
# response = client.get("https://www.example.com/", extensions={"trace": log})
# limits = httpx.Limits(max_connections=100, max_keepalive_connections=100, keepalive_expiry=10.0)
# with httpx.Client(limits=limits) as client:
#     resp = client.get(
#         "https://www.example.com/",
#         extensions={"timeout": {"connect": 10.0, "pool": 5.0}},
#     )
# print(resp.extensions["http_version"])  # b'HTTP/1.1'
# print(resp.extensions["reason_phrase"])  # b'OK'
# resp = httpx.get("https://example.com", timeout=None)
# with httpx.Client() as client:
#     resp = client.get("https://example.com", timeout=None)
# with httpx.Client(default_encoding="shift-jis") as client:
#     resp = client.get("https://httpbin.org/get")
# print(resp.encoding)  # shift-jis
# print(resp.text)  # 文本会使用 Content-Type charset 解码，
# # 否则使用 "shift-jis" 解码。
from charset_normalizer import detect

import httpx


def autodetect(content) -> str:
    print(detect(content))
    return detect(content)["encoding"]


with httpx.Client(default_encoding=autodetect) as client:
    resp = client.get("https://httpbin.org/get")

print(resp.encoding)  # ascii
