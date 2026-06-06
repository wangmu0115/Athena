import httpx

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
#     print(req.headers)  # Headers({'host': 'example.com', 'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'connection': 'keep-alive', 'user-agent': 'python-httpx/0.28.1', 'x-api-key': 'Cli-Api', 'x-client-id': '123'})

#     #
#     del req.headers["X-Api-Key"]
#     resp = client.send(req)
# print(resp)  # <Response [200 OK]>
# print(resp.request.headers)  # Headers({'host': 'example.com', 'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'connection': 'keep-alive', 'user-agent': 'python-httpx/0.28.1', 'x-client-id': '123'})
