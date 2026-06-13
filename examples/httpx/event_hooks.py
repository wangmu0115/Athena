from datetime import UTC, datetime

import httpx


def log_request(req: httpx.Request):
    print(f"Request event hook: {req.method} {req.url} - Waiting for response")


def log_response(resp: httpx.Response):
    req = resp.request
    print(f"Response event hook: {req.method} {req.url} - Status {resp.status_code}")


def raise_on_non_2xx(resp: httpx.Response):
    resp.raise_for_status()


def add_timestamp(req: httpx.Request):
    req.headers["x-request-timestamp"] = datetime.now(tz=UTC).isoformat()


client = httpx.Client(event_hooks={"request": [add_timestamp], "response": [raise_on_non_2xx]})
print(client.event_hooks)
client.event_hooks["request"].append(log_request)
client.event_hooks["response"].append(log_response)
print(client.event_hooks)


resp = client.get("http://github.com", follow_redirects=True)
print(resp.text)
