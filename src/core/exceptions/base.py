"""Base Exceptions Used Throughout the Application."""


class AppBaseExceptionsError(Exception):
    """Base class for all application-specific exceptions.

    Use this as the parent for all custom exceptions in the application.

    Args:
        message (str | None): Human-readable error message.
        context (dict | None): Additional context data for debugging.
        original_exception (Exception | None): Original exception, if any.
        status_code (int | None): HTTP status code associated with the error.

    Returns:
        Exception instance with enriched context information.
    """

    DEFAULT_STATUS_CODE: int = 500
    DEFAULT_MESSAGE: str = "An error occurred in the application."

    def __init__(
        self,
        message: str | None = None,
        context: dict | None = None,
        original_exception: Exception | None = None,
        status_code: int | None = None,
    ):
        message = message or self.DEFAULT_MESSAGE
        super().__init__(message)
        self.context = context or {}
        self.original_exception = original_exception
        self.status_code = status_code or self.DEFAULT_STATUS_CODE

    def to_dict(self) -> dict:
        """Convert exception details to a dictionary."""
        return {
            "error_type": self.__class__.__name__,
            "message": str(self),
            "context": self.context,
            "original_exception": repr(self.original_exception)
            if self.original_exception is not None
            else None,
        }

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(message={self.args[0]!r}, "
            f"context={self.context!r}, "
            f"original_exception={self.original_exception!r})"
        )
