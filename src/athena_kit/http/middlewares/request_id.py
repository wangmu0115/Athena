from typing import Any

import httpx

from athena_kit.http import RequestHandler, RequestIDOptions


def request_id_middleware():
    """Add a request id header if it does not already exist."""

    def middleware(next_handler: RequestHandler) -> RequestHandler:
        async def wrapper(method: str, url: str, **kwargs: Any) -> httpx.Response:
            options = kwargs["context"].request_id

            if not options.enabled:
                return await next_handler(method, url, **kwargs)

            id_header_name = options.header_name or _DEFAULT_OPTIONS.header_name
            request_id_factory = options.id_factory or _DEFAULT_OPTIONS.id_factory

            headers = dict(kwargs.pop("headers", None) or {})
            headers.setdefault(id_header_name, request_id_factory())
            kwargs["headers"] = headers

            return await next_handler(method, url, **kwargs)

        return wrapper

    middleware.__middleware_name__ = "RequestIDMiddleware"
    return middleware


_DEFAULT_OPTIONS = RequestIDOptions.default()
