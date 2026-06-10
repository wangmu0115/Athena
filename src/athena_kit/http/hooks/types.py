from collections.abc import Awaitable, Callable, Sequence
from typing import TypedDict

import httpx

type RequestHook = Callable[[httpx.Request], None]
type ResponseHook = Callable[[httpx.Response], None]
type AsyncRequestHook = Callable[[httpx.Request], Awaitable[None]]
type AsyncResponseHook = Callable[[httpx.Response], Awaitable[None]]


class EventHooks(TypedDict, total=False):
    request: Sequence[RequestHook]
    response: Sequence[ResponseHook]


class AsyncEventHooks(TypedDict, total=False):
    request: Sequence[AsyncRequestHook]
    response: Sequence[AsyncResponseHook]
