from typing import Any, Protocol, runtime_checkable

import httpx


class RequestHandler(Protocol):
    async def __call__(self, method: str, url: str, **kwargs: Any) -> httpx.Response: ...


@runtime_checkable
class Middleware(Protocol):
    def __call__(self, next_handler: RequestHandler) -> RequestHandler: ...


def get_middleware_name(middleware: Middleware) -> str:
    return getattr(
        middleware,
        "__middleware_name__",
        getattr(middleware, "__name__", middleware.__class__.__name__),
    )
