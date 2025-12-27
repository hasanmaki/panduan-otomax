from src.config.settings import get_settings
from src.services.errors import AuthError


class CredentialAuth:
    """Validate provided pin and password against settings."""

    def __init__(self, settings=None):
        self.settings = settings or get_settings()

    def validate(self, memberid: str, pin: str, password: str) -> None:
        """Raise AuthError("pin password salah", 401) on mismatch."""
        if str(pin) != str(self.settings.OTO.pin) or str(password) != str(
            self.settings.OTO.password
        ):
            raise AuthError("pin password salah", 401)
