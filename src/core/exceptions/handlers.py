from fastapi import FastAPI, Request  # noqa: D100
from fastapi.responses import JSONResponse
from loguru import logger
from src.core.exceptions.base import AppBaseExceptionsError


async def app_exception_handler(request: Request, exc: Exception) -> JSONResponse:  # noqa: RUF029
    """Handler for application-specific exceptions.

    Args:
        request: The incoming HTTP request.
        exc: The application-specific exception instance.

    Returns:
        A JSON response with error details.
    """
    trace_id = getattr(request.state, "trace_id", "unknown")
    # Cast exc to AppBaseExceptionsError
    if isinstance(exc, AppBaseExceptionsError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "rc": exc.__class__.__name__,
                "message": str(exc),
                "trace_id": trace_id,
            },
        )
    else:
        # fallback for unexpected types
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "rc": "INTERNAL_SERVER_ERROR",
                "message": "Terjadi kesalahan internal, silakan hubungi admin.",
                "trace_id": trace_id,
            },
        )


async def unexpected_exception_handler(  # noqa: RUF029
    request: Request, exc: Exception
) -> JSONResponse:
    """Handler for unexpected system errors.

    Args:
        request: The incoming HTTP request.
        exc: The unexpected exception instance.

    Returns:
        A JSON response with a generic error message.
    """
    trace_id = getattr(request.state, "trace_id", "unknown")
    logger.opt(exception=exc).critical(f"UNEXPECTED ERROR | Trace: {trace_id}")
    logger.debug("unexpected_exception_handler invoked")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "rc": "INTERNAL_SERVER_ERROR",
            "message": "Terjadi kesalahan internal, silakan hubungi admin.",
            "trace_id": trace_id,
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register exception handlers for the FastAPI app.

    Args:
        app: The FastAPI application instance.
    """
    app.add_exception_handler(AppBaseExceptionsError, app_exception_handler)
    app.add_exception_handler(Exception, unexpected_exception_handler)
