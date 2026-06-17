import asyncio
import time
from collections import deque
from collections.abc import Awaitable, Callable, Mapping, Sequence
from dataclasses import dataclass
from threading import Lock
from typing import Protocol

import httpx

type RateLimitRoute = tuple[str, str]


class RateLimiter(Protocol):
    """同步 HTTP 频控器协议。"""

    def acquire(self, request: httpx.Request | None = None) -> None:
        """等待直到本次请求获得发送许可。"""


class AsyncRateLimiter(Protocol):
    """异步 HTTP 频控器协议。"""

    async def acquire(self, request: httpx.Request | None = None) -> None:
        """等待直到本次请求获得发送许可。"""


@dataclass(frozen=True, slots=True)
class RateLimit:
    """频控规则。

    Attributes:
        limit: 时间窗口内允许的最大请求次数。
        period: 时间窗口长度，单位为秒。
    """

    limit: int
    period: float

    def __post_init__(self) -> None:
        if self.limit < 1:
            raise ValueError("`limit` should be greater than or equal to 1.")
        if self.period <= 0:
            raise ValueError("`period` should be greater than 0.")


class SlidingWindowRateLimiter:
    """基于滑动窗口的同步频控器。

    每次请求前记录发送时间，只保留最近 `period` 秒内的时间戳。
    当窗口内请求数达到 `limit` 时，阻塞到最早一次请求滑出窗口。
    """

    def __init__(
        self,
        limit: int,
        period: float,
        *,
        clock: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], None] = time.sleep,
    ):
        self._rule = RateLimit(limit, period)
        self._clock = clock
        self._sleep = sleep
        self._timestamps: deque[float] = deque()
        self._lock = Lock()

    def acquire(self, request: httpx.Request | None = None) -> None:
        while True:
            with self._lock:
                now = self._clock()
                self._discard_expired(now)
                if len(self._timestamps) < self._rule.limit:
                    self._timestamps.append(now)
                    return

                wait_seconds = self._timestamps[0] + self._rule.period - now

            self._sleep(max(wait_seconds, 0))

    def _discard_expired(self, now: float) -> None:
        expires_before = now - self._rule.period
        while self._timestamps and self._timestamps[0] <= expires_before:
            self._timestamps.popleft()


class AsyncSlidingWindowRateLimiter:
    """基于滑动窗口的异步频控器。"""

    def __init__(
        self,
        limit: int,
        period: float,
        *,
        clock: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
    ):
        self._rule = RateLimit(limit, period)
        self._clock = clock
        self._sleep = sleep
        self._timestamps: deque[float] = deque()
        self._lock = asyncio.Lock()

    async def acquire(self, request: httpx.Request | None = None) -> None:
        while True:
            async with self._lock:
                now = self._clock()
                self._discard_expired(now)
                if len(self._timestamps) < self._rule.limit:
                    self._timestamps.append(now)
                    return

                wait_seconds = self._timestamps[0] + self._rule.period - now

            await self._sleep(max(wait_seconds, 0))

    def _discard_expired(self, now: float) -> None:
        expires_before = now - self._rule.period
        while self._timestamps and self._timestamps[0] <= expires_before:
            self._timestamps.popleft()


class CompositeRateLimiter:
    """组合多个同步频控器，本次请求需要依次获得所有许可。"""

    def __init__(self, limiters: Sequence[RateLimiter]):
        self._limiters = tuple(limiters)

    def acquire(self, request: httpx.Request | None = None) -> None:
        for limiter in self._limiters:
            limiter.acquire(request)


class AsyncCompositeRateLimiter:
    """组合多个异步频控器，本次请求需要依次获得所有许可。"""

    def __init__(self, limiters: Sequence[AsyncRateLimiter]):
        self._limiters = tuple(limiters)

    async def acquire(self, request: httpx.Request | None = None) -> None:
        for limiter in self._limiters:
            await limiter.acquire(request)


class RouteRateLimiter:
    """按 HTTP method 和 URL path 分派同步频控器。"""

    def __init__(
        self,
        routes: Mapping[RateLimitRoute, RateLimiter | Sequence[RateLimiter]],
        *,
        default: RateLimiter | None = None,
    ):
        self._routes = {_normalize_route(route): _normalize_rate_limiter(limiter) for route, limiter in routes.items()}
        self._default = default

    def acquire(self, request: httpx.Request | None = None) -> None:
        limiter = self._match(request)
        if limiter is not None:
            limiter.acquire(request)

    def _match(self, request: httpx.Request | None) -> RateLimiter | None:
        if request is None:
            return self._default

        route = (request.method.upper(), request.url.path)
        return self._routes.get(route, self._default)


class AsyncRouteRateLimiter:
    """按 HTTP method 和 URL path 分派异步频控器。"""

    def __init__(
        self,
        routes: Mapping[RateLimitRoute, AsyncRateLimiter | Sequence[AsyncRateLimiter]],
        *,
        default: AsyncRateLimiter | None = None,
    ):
        self._routes = {
            _normalize_route(route): _normalize_async_rate_limiter(limiter) for route, limiter in routes.items()
        }
        self._default = default

    async def acquire(self, request: httpx.Request | None = None) -> None:
        limiter = self._match(request)
        if limiter is not None:
            await limiter.acquire(request)

    def _match(self, request: httpx.Request | None) -> AsyncRateLimiter | None:
        if request is None:
            return self._default

        route = (request.method.upper(), request.url.path)
        return self._routes.get(route, self._default)


def _normalize_route(route: RateLimitRoute) -> RateLimitRoute:
    method, path = route
    if not path.startswith("/"):
        path = f"/{path}"
    return method.upper(), path


def _normalize_rate_limiter(limiter: RateLimiter | Sequence[RateLimiter]) -> RateLimiter:
    if isinstance(limiter, Sequence):
        return CompositeRateLimiter(limiter)
    return limiter


def _normalize_async_rate_limiter(limiter: AsyncRateLimiter | Sequence[AsyncRateLimiter]) -> AsyncRateLimiter:
    if isinstance(limiter, Sequence):
        return AsyncCompositeRateLimiter(limiter)
    return limiter
