# Copyright (c) 2025 Hasan Maki. All rights reserved.
"""Middleware module for request context handling.

This module provides middleware for handling request context, including trace ID propagation,
client information capture, request duration measurement, and access logging.

Key Features:
    - Propagates or generates trace IDs
    - Captures client IP and user agent
    - Measures request duration
    - Adds helpful response headers
    - Logs concise access lines with context

Attributes:
    RequestContextMiddleware (class): Middleware class for request context handling.

Example:
    ```python
    from starlette.applications import Starlette
    from starlette.responses import JSONResponse
    from starlette.routing import Route
    from api.middlewares.ctx_middleware import (
        RequestContextMiddleware,
    )


    async def homepage(request):
        return JSONResponse({
            "hello": "world",
            "trace_id": request.state.trace_id,
        })


    app = Starlette(routes=[Route("/", homepage)])
    app.add_middleware(RequestContextMiddleware)
    ```

Note:
    This middleware is designed to be used with ASGI frameworks like Starlette or FastAPI.
"""

import time
import uuid
from collections.abc import Awaitable, Callable
from typing import Any

from loguru import logger
from starlette.requests import Request


class RequestContextMiddleware:
    """Pure ASGI middleware for request context handling, streaming-safe."""

    def __init__(
        self, app: Callable[[dict[str, Any], Callable, Callable], Awaitable[None]]
    ):
        """Initialize the middleware with the ASGI app.

        Args:
            app: The ASGI application to wrap.
        """
        self.app = app

    def _is_valid_trace_id(self, tid: str) -> bool:
        """Validate the trace ID.

        Args:
            tid: The trace ID to validate.

        Returns:
            True if the trace ID is valid, False otherwise.
        """
        is_valid = tid.isalnum() and 8 <= len(tid) <= 64
        if not is_valid:
            logger.trace(f"Invalid trace_id rejected: {tid}")
        return is_valid

    async def __call__(
        self,
        scope: dict[str, Any],
        receive: Callable[[], Awaitable[dict[str, Any]]],
        send: Callable[[dict[str, Any]], Awaitable[None]],
    ) -> None:
        """Handle the incoming request and response.

        Args:
            scope: The ASGI scope dictionary.
            receive: The ASGI receive callable.
            send: The ASGI send callable.
        """
        logger.trace("RequestContextMiddleware invoked")
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Build request object
        request = Request(scope, receive=receive)

        # 1) Propagate incoming trace id if provided, else generate a new one
        incoming_trace = request.headers.get("x-trace-id")

        if incoming_trace:
            candidate = incoming_trace.strip()
            trace_id = (
                candidate if self._is_valid_trace_id(candidate) else str(uuid.uuid4())
            )
        else:
            trace_id = str(uuid.uuid4())
        request.state.trace_id = trace_id

        logger.trace(f"Trace ID set to: {trace_id}")

        # 2) Capture client info early
        client_ip = self._get_client_ip(request)
        user_agent = request.headers.get("user-agent", "unknown")
        request.state.client_ip = client_ip
        request.state.user_agent = user_agent

        logger.trace(f"Client IP: {client_ip}, User Agent: {user_agent}")

        # 3) Measure processing time
        start_time = time.perf_counter()
        response_status = 500
        response_headers = []
        duration_ms = None

        async def send_wrapper(message: dict[str, Any]) -> None:
            nonlocal response_status, response_headers, duration_ms
            if message["type"] == "http.response.start":
                response_status = message["status"]
                # Add trace headers safely without overwriting duplicates
                headers = list(message.get("headers", []))
                headers.append((b"x-trace-id", trace_id.encode()))
                headers.append((
                    b"x-process-time",
                    f"{(time.perf_counter() - start_time) * 1000.0:.2f}ms".encode(),
                ))
                message["headers"] = headers
                response_headers = message["headers"]
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        except Exception:
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            logger.bind(
                trace_id=trace_id,
                client_ip=client_ip,
                user_agent=user_agent,
                status_code=500,
                duration_ms=duration_ms,
                method=scope.get("method", "unknown"),
                path=scope.get("path", "unknown"),
            ).exception("Request failed")
            raise
        else:
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            logger.bind(
                trace_id=trace_id,
                client_ip=client_ip,
                user_agent=user_agent,
                status_code=response_status,
                duration_ms=duration_ms,
                method=scope.get("method", "unknown"),
                path=scope.get("path", "unknown"),
            ).info(
                f"\u2190 {scope.get('method', 'unknown')} {scope.get('path', 'unknown')} | "
                f"status={response_status} | {duration_ms:.2f}ms"
            )

    @staticmethod
    def _get_client_ip(request: Request) -> str:
        """Extract real client IP, accounting for proxies.

        Chooses the left-most x-forwarded-for when present.

        Args:
            request: The Starlette request object.

        Returns:
            The client IP address as a string.
        """
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
        if request.client:
            return request.client.host
        return "unknown"
