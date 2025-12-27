from src.config.settings import get_settings
from src.services.errors import AuthError


class ClientAuth:
    """Validate client IP and member id matches stored settings."""

    def __init__(self, settings=None):
        self.settings = settings or get_settings()

    def validate(self, memberid: str, client_ip: str) -> None:
        """Raise AuthError("invalid IP", 403) when IP check enabled and mismatch."""
        memberid = str(memberid).strip()
        allowed_memberid = str(self.settings.OTO.memberid).strip().upper()
        allowed_memberip = str(self.settings.OTO.memberip or "").split(":")[0]
        enable_ip_check = bool(getattr(self.settings.OTO, "enable_ip_check", True))

        if enable_ip_check and (
            memberid.upper() != allowed_memberid or client_ip != allowed_memberip
        ):
            raise AuthError("invalid IP", 403)
