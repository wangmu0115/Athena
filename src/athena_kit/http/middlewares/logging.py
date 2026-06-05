import logging
import time
from collections.abc import Mapping
from typing import Any

import httpx

from athena_kit.http import LoggingOptions, RequestHandler


class LoggingMiddleware:
    """Log HTTP request and response metadata."""

    __middleware_name__ = "LoggingMiddleware"

    SENSITIVE_HEADERS = frozenset({"authorization", "cookie", "set-cookie", "x-api-key"})

    def __init__(self):
        self._default_options = LoggingOptions.default(logging.getLogger(__name__))

    def __call__(self, next_handler: RequestHandler) -> RequestHandler:
        async def wrapper(method: str, url: str, **kwargs: Any) -> httpx.Response:
            options: LoggingOptions = kwargs["context"].logging

            if not options.enabled:
                return await next_handler(method, url, **kwargs)

            logger = options.logger or self._default_options.logger
            level = options.level if options.level is not None else self._default_options.level

            start = time.perf_counter()
            headers = self._mark_headers(kwargs.get("headers"))

            logger.log(
                level, "HTTP request started: method=%s, url=%s, headers=%s",
                method, url, headers,
            )  # fmt: off
            try:
                response = await next_handler(method, url, **kwargs)
                elapsed = time.perf_counter() - start
                logger.log(
                    level, "HTTP request completed: method=%s, url=%s, status_code=%s, elapsed(ms)=%.2f",
                    method, url, response.status_code, elapsed * 1000.0
                )  # fmt: off

                return response

            except Exception:
                elapsed = time.perf_counter() - start
                logger.exception(
                    "HTTP request failed: method=%s, url=%s, elapsed(ms)=%.2f",
                    method, url, elapsed * 1000.0,
                )  # fmt: off

                raise

        return wrapper

    def _mark_headers(self, headers: Mapping[str, str] | None) -> dict[str, str]:
        if headers is None:
            return {}
        return {
            key: "******" if key.lower() in self.SENSITIVE_HEADERS else value 
            for key, value in headers.items()
        }  # fmt: off
