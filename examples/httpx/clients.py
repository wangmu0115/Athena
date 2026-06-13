# with httpx.Client() as client:
#     headers = {"X-Custom": "xvalue"}
#     resp = client.get("https://example.com", headers=headers)
#     print(resp)  # <Response [200 OK]>
#     print(resp.request.headers["X-Custom"])  # xvalue

# client = httpx.Client()
# try:
#     ...
# finally:
#     client.close()


# url = "http://httpbin.org/headers"
# headers = {"user-agent": "my-app/0.0.1"}
# with httpx.Client(headers=headers) as client:
#     resp = client.get(url)
# print(resp.request.headers["user-agent"])  # my-app/0.0.1


# client_level_headers = {"X-Auth": "from-client"}
# client_level_params = {"client_id": "client1"}
# with httpx.Client(headers=client_level_headers, params=client_level_params) as client:
#     request_level_headers = {"X-Custom": "from-request"}
#     request_level_params = {"request_id": "request1"}
#     resp = client.get("https://example.com", headers=request_level_headers, params=request_level_params)
# # https://example.com?client_id=client1&request_id=request1
# print(resp.request.url)
# # Headers({..., 'x-auth': 'from-client', 'x-custom': 'from-request', ...})
# print(resp.request.headers)

# import base64

# with httpx.Client(auth=("tom", "mot123")) as client:
#     resp = client.get("https://example.com", auth=("alice", "ecila123"))
# _, _, auth = resp.request.headers["Authorization"].partition(" ")
# print(base64.b64decode(auth))  # b'alice:ecila123'


# req = httpx.Request("GET", "https://example.com")
# with httpx.Client() as client:
#     resp = client.send(req)
# print(resp)  # <Response [200 OK]>


# headers = {"X-Api-Key": "Cli-Api", "X-Client-ID": "123"}
# with httpx.Client(headers=headers) as client:
#     req = client.build_request("GET", "https://example.com")
#     print(req.headers)

#     #
#     del req.headers["X-Api-Key"]
#     resp = client.send(req)
# print(resp)  # <Response [200 OK]>
# print(resp.request.headers)

# with httpx.Client(base_url="http://httpbin.org") as client:
#     resp = client.get("headers")

# print(resp.request.url)

# params = {"key1": "value1", "key2": ["value2", "value3"]}
# # params = "key1=value1&key2=value2"
# # params = [("key1", "value1"), ("key2", "value2")]

# resp = httpx.get("https://httpbin.org/get", params=params)
# print(resp.url)

# resp = httpx.get("https://api.github.com/events")
# resp.encoding = "ISO-8859-1"
# print(f"{resp.text!r}")
# print(resp.encoding)
# print(resp.content)
# print(resp.json())

# headers = {"user-agent": "my-app/0.0.1"}
# resp = httpx.get("https://httpbin.org/headers", headers=headers)
# # Headers({..., 'user-agent': 'my-app/0.0.1', ...})
# print(resp.request.headers)

import httpx

# data = {"key1": "value1", "key2": ["value2", "value3"]}
# resp = httpx.post("https://httpbin.org/post", data=data)
# print(resp.text)

# data = {"integer": 123, "boolean": True, "list": ["a", "b", "c"]}
# resp = httpx.post("https://httpbin.org/post", json=data)
# print(resp.text)
# resp = httpx.get("https://httpbin.org/get")
# print(resp.status_code)
# print(resp.status_code == httpx.codes.OK)

# not_found = httpx.get("https://httpbin.org/status/404")
# print(not_found.status_code)
# not_found.raise_for_status()

# try:
#     response = httpx.get("https://www.example.com")
#     response.raise_for_status()
# except httpx.RequestError as exc:
#     print(f"An error occurred while requesting {exc.request.url!r}.")
# except httpx.HTTPStatusError as exc:
#     print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")

# response = httpx.get("https://www.example.com/")
# try:
#     response.raise_for_status()
# except httpx.HTTPStatusError as exc:
#     print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")


response = httpx.get("http://github.com", follow_redirects=True)
print(response.status_code)
print(response.url)
print(response.request.url)
print(response.history)
print(response.next_request)


response = httpx.get("http://github.com")
print(response.status_code)
print(response.url)
print(response.history)
print(response.next_request)
