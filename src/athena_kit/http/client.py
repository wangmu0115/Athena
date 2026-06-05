import logging
from collections.abc import Mapping, Sequence
from typing import Any

import httpx

from athena_kit.http import (
    Extensions,
    LoggingOptions,
    Middleware,
    RequestContext,
    RequestHandler,
    RequestIDOptions,
    RetryOptions,
    get_middleware_name,
)
from athena_kit.http.middlewares import DEFAULT_MIDDLEWARES

logger = logging.getLogger(__name__)


class AsyncHttpClient:
    """Asynchronous HTTP client with middleware pipeline support.

    This class is a lightweight wrapper around `httpx.AsyncClient` that adds
    a composable middleware pipeline for handling cross-cutting concerns such as:
        - request ID injection
        - structured logging
        - HTTP exception normalization
        - retry with backoff and `Retry-After` support

    ------------------------------------------------------------------------
    API Design
    ------------------------------------------------------------------------

    The public request interface mirrors `httpx.AsyncClient.request()` as much as possible.
    Most keyword arguments are forwarded directly to httpx, including:
        params, headers, json, data, files, cookies, auth, timeout, etc.

    In addition, this client introduces one extra keyword argument:
        **extensions**:
            An optional `Extensions` object used to override middleware behavior
            for a single request (e.g., retry, logging, request ID).
            This argument is consumed internally and is NOT passed to httpx.

    ------------------------------------------------------------------------
    Middleware Pipeline
    ------------------------------------------------------------------------

    The middleware system follows an onion model:
        Request flow:
            RequestIDMiddleware
                -> LoggingMiddleware
                -> HttpExceptionMiddleware
                -> RetryMiddleware
                -> httpx.AsyncClient.request
        Response flow:
            httpx.AsyncClient.request
                -> RetryMiddleware
                -> HttpExceptionMiddleware
                -> LoggingMiddleware
                -> RequestIDMiddleware

    Each middleware can:
        - modify outgoing requests
        - inspect or transform responses
        - raise or normalize exceptions
        - short-circuit execution (e.g., retry)

    ------------------------------------------------------------------------
    Ordering Rules
    ------------------------------------------------------------------------

    Middlewares are applied in declaration order, but execution is layered:
        - Earlier middlewares wrap later ones
        - Later middlewares are closer to the HTTP transport layer

    Therefore:
        - Middlewares that need raw `httpx.Response` objects (e.g. retry)
          should be declared AFTER exception-normalization middleware
        - Middlewares that operate on logical/normalized responses
          should be declared BEFORE it

    ------------------------------------------------------------------------
    Configuration Model
    ------------------------------------------------------------------------

    Configuration is resolved in three layers:
        Client defaults (Options)
            + per-request overrides (Extensions)
            ->
        RequestContext (immutable during execution)
            ->
        Middleware consumption

    This design provides:
        - strong typing
        - clear override semantics
        - separation of configuration and execution

    ------------------------------------------------------------------------
    Lifecycle
    ------------------------------------------------------------------------

    The underlying `httpx.AsyncClient` is owned and managed by this class.

    Recommended usage:
        ```python
        async with AsyncHttpClient(...) as client:
            await client.get(...)
        ```

    The client will automatically close the underlying connection pool.

    ------------------------------------------------------------------------
    Design Principles
    ------------------------------------------------------------------------

    - Separation of concerns: client (orchestration) vs middleware (behavior)
    - Composability: middlewares can be freely combined
    - Extensibility: new middleware and options can be added independently
    - Declarative configuration: behavior is controlled via typed Options and Extensions
    """

    def __init__(
        self,
        *,
        base_url: str = "",
        timeout: float | httpx.Timeout = 5.1,
        headers: Mapping[str, str] | None = None,
        follow_redirects: bool = False,
        transport: httpx.AsyncBaseTransport | None = None,
        middlewares: Sequence[Middleware] | None = None,
        retry_options: RetryOptions | None = None,
        logging_options: LoggingOptions | None = None,
        request_id_options: RequestIDOptions | None = None,
    ):

        self._client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            headers=headers,
            follow_redirects=follow_redirects,
            transport=transport,
        )
        self._retry_options = retry_options or RetryOptions.default()
        self._logging_options = logging_options or LoggingOptions.default()
        self._request_id_options = request_id_options or RequestIDOptions.default()

        self._middlewares = list(middlewares or DEFAULT_MIDDLEWARES)
        self._has_exception_middleware = self._contains_exception_middleware()
        self._handler = self._build_handler()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._client.aclose()

    @property
    def middleware_chain(self) -> list[str]:
        return [get_middleware_name(middleware) for middleware in self._middlewares]

    async def request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        """Send a HTTP request through the middleware pipeline.

        Args:
            method: HTTP method, such as `GET`, `OPTIONS`, `HEAD`, `POST`, `PUT`, `PATCH`, or `DELETE`
            url: Request URL. Relative URLs are resolved against the client's `base_url` if configured
            **kwargs: Keyword arguments forwarded to `httpx.AsyncClient.request()`,
                such as `params`, `headers`, `json`, `data`, `files`, `cookies`,
                `auth`, `timeout`, and `follow_redirects`

                In addition to httpx request arguments, this method accepts one client-specific keyword argument:
                    `extensions`: Optional `Extensions` object used to override middleware behavior for this request
        """
        extensions: Extensions | None = kwargs.pop("extensions", None)
        request_context = self._build_request_context(extensions)
        kwargs["context"] = request_context

        return await self._handler(method.upper(), url, **kwargs)

    async def get(self, url: str, **kwargs: Any) -> httpx.Response:
        """Send a GET request."""
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs: Any) -> httpx.Response:
        """Send a POST request."""
        return await self.request("POST", url, **kwargs)

    async def put(self, url: str, **kwargs: Any) -> httpx.Response:
        """Send a PUT request."""
        return await self.request("PUT", url, **kwargs)

    async def patch(self, url: str, **kwargs: Any) -> httpx.Response:
        """Send a PATCH request."""
        return await self.request("PATCH", url, **kwargs)

    async def delete(self, url: str, **kwargs: Any) -> httpx.Response:
        """Send a DELETE request."""
        return await self.request("DELETE", url, **kwargs)

    async def _do_request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        # Remove the middleware-only `context` parameter before calling `httpx.AsyncClient.request()`,
        # otherwise httpx will raise: `TypeError: got an unexpected keyword argument 'context'.`
        kwargs.pop("context", None)
        response = await self._client.request(method, url, **kwargs)

        # If HttpExceptionMiddleware is not installed, fall back to httpx's native status validation
        # so callers still receive either a successful response or an HTTP-layer exception.
        if not self._has_exception_middleware:
            response.raise_for_status()

        return response

    def _contains_exception_middleware(self) -> bool:
        return any(get_middleware_name(middleware) == "HttpExceptionMiddleware" for middleware in self._middlewares)

    def _build_handler(self) -> RequestHandler:
        handler: RequestHandler = self._do_request

        _middleware_names = [get_middleware_name(middleware) for middleware in self._middlewares]
        logger.debug(
            "Request flow: %s, Response flow: %s",
            " -> ".join(_middleware_names),
            " -> ".join(reversed(_middleware_names)),
        )

        for middleware in reversed(self._middlewares):
            handler = middleware(handler)

        return handler

    def _build_request_context(self, extensions: Extensions | None) -> RequestContext:
        retry_options = self._retry_options
        logging_options = self._logging_options
        request_id_options = self._request_id_options
        if extensions is not None:
            retry_options = retry_options.with_overrides(extensions.retry)
            logging_options = logging_options.with_overrides(extensions.logging)
            request_id_options = request_id_options.with_overrides(extensions.request_id)

        return RequestContext(
            retry=retry_options,
            logging=logging_options,
            request_id=request_id_options,
        )
