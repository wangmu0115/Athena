import httpx

from athena_kit.http import (
    HttpClientError,
    HttpRequestError,
    HttpResponseError,
    HttpTimeoutError,
    RequestHandler,
)


def http_exception_middleware():
    """Normalize HTTP-layer exceptions.

    This middleware converts httpx-native exceptions and HTTP status errors into `HttpClientError` or its subclasses.

    Responsibilities:
        - Convert timeout errors to `HttpTimeoutError`
        - Convert network/request errors to `HttpRequestError`
        - Convert non-successful HTTP status codes to `HttpResponseError`
        - Pass through existing `HttpClientError` instances unchanged

    Notes:
        This middleware should be declared before middlewares that need raw responses,
        such as `RetryMiddleware` or integration-specific auth middlewares.
    """

    def middleware(next_handler: RequestHandler) -> RequestHandler:
        async def wrapper(method: str, url: str, **kwargs) -> httpx.Response:
            try:
                response = await next_handler(method, url, **kwargs)

                try:
                    response.raise_for_status()
                except httpx.HTTPStatusError as exc:
                    raise HttpResponseError(
                        response.status_code,
                        str(exc),
                        response,
                    ) from exc

                return response

            except HttpClientError:
                raise
            except httpx.TimeoutException as exc:
                raise HttpTimeoutError(
                    f"HTTP timeout: {method} {url}",
                ) from exc
            except httpx.RequestError as exc:
                raise HttpRequestError(
                    f"HTTP request failed: {method} {url}",
                ) from exc

        return wrapper

    middleware.__middleware_name__ = "HttpExceptionMiddleware"
    return middleware
