class AuthError(Exception):
    """Exception untuk kegagalan autentikasi dengan code dan message."""

    def __init__(self, detail: str, status_code: int = 401) -> None:
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)
