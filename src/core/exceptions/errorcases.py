"""this module contains domain-specific error cases for the application.

why we do this: to have clear, specific exceptions that represent common error scenarios in the domain layer. this improves error handling, debugging,
and user feedback by providing meaningful messages and status codes.
the exceptions doesnt scattered throughout the codebase, making it easier to maintain and extend.
"""

from src.core.exceptions.base import AppBaseExceptionsError


class EntityNotFoundError(AppBaseExceptionsError):
    """Domain error: requested entity was not found."""

    DEFAULT_MESSAGE = "Entity not found"
    DEFAULT_STATUS_CODE = 404


class InvalidInputError(AppBaseExceptionsError):
    """Domain error: input data is invalid or malformed."""

    DEFAULT_MESSAGE = "Invalid input"
    DEFAULT_STATUS_CODE = 400


class PermissionDeniedError(AppBaseExceptionsError):
    """Domain error: user does not have permission to perform the action."""

    DEFAULT_MESSAGE = "Permission denied"
    DEFAULT_STATUS_CODE = 403


class ResourceConflictError(AppBaseExceptionsError):
    """Domain error: resource conflict occurred."""

    DEFAULT_MESSAGE = "Resource conflict"
    DEFAULT_STATUS_CODE = 409


class DomainValidationError(AppBaseExceptionsError):
    """Domain error: domain-specific validation failed."""

    DEFAULT_MESSAGE = "Validation error"
    DEFAULT_STATUS_CODE = 422
