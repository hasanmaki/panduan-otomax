"""main for testing simulation."""

from contextlib import asynccontextmanager
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import FastAPI
from loguru import logger

from src.core.exceptions import (
    register_exception_handlers,
)
from src.core.middlewares import RequestContextMiddleware
from src.core.mlogging.config import setup_logging

setup_logging()
dt_jakarta = datetime.now(ZoneInfo("Asia/Jakarta"))


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: D103
    logger.info("Starting up the FastAPI application...")
    yield

    now: datetime = datetime.now(ZoneInfo("Asia/Jakarta"))
    logger.info(f"Shutting down @: {now.isoformat()}")


# Create the real FastAPI app
app = FastAPI(lifespan=lifespan)


# Register middleware and exception handlers on the real app
app.add_middleware(RequestContextMiddleware)
register_exception_handlers(app)


@app.get("/ping")
async def ping():
    """Just a ping endpoint to check if the server is running."""
    return {"message": "pong"}


def main() -> None:
    import uvicorn

    # Use the string import to enable reload functionality
    uvicorn.run(
        app="src.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_excludes=["logs/*"],
    )


if __name__ == "__main__":
    main()
