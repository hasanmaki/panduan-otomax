"""Logging configuration module.

Provides an InterceptHandler that forwards standard library logging records to
Loguru and a setup_logging() convenience function that installs the handler and
loads Loguru configuration from mlog.yaml located at the project root.

Usage:
    from core.mlogging.config import setup_logging
    setup_logging()

Constants:
    LOGCONFIGPATH (Path): Path to mlog.yaml used to configure Loguru.
"""

import inspect
import logging
from pathlib import Path

from loguru import logger
from loguru_config import LoguruConfig

LOGCONFIGPATH = Path(__file__).parent.parent.parent.parent / "mlog.yaml"


class InterceptHandler(logging.Handler):
    """Default handler.

    to intercept standard logging messages and redirect them to Loguru.
    """

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a record.

        Redirect standard logging messages to Loguru.
        """
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging() -> None:
    """Setup logging configuration."""
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    LoguruConfig().load(config_or_file=LOGCONFIGPATH, inplace=True, configure=True)
