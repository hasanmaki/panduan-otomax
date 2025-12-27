from typing import Any

from src.config.settings import get_settings
from src.services.errors import AuthError


class AuthenticationService:
    """Service untuk autentikasi transaksi OtomaX API.

    Behavior:
        - If `enable_ip_check` is True in settings, validate client IP matches stored member IP.
        - Accept either pin+password or sign.
        - On pin+password: check credentials, compute signature and compare when `sign` is provided.
        - On sign only: verify signature using stored credentials for the member.
        - Raise `AuthError` with appropriate message and status code on failures.
        - Return dict on success containing status, trxid, memberid, sign.
    """

    def __init__(self, signature_service: Any, settings: Any = None) -> None:
        self.signature = signature_service
        self.settings = settings or get_settings()

    def authenticate_transaction(self, auth: Any, client_ip: str) -> dict:
        """Orchestrate small auth components to validate a transaction request.

        Uses `ClientAuth`, `CredentialAuth`, and `SignatureAuth` to separate concerns.
        """
        # lazy import to avoid circular imports at module import time
        from src.services.client_auth import ClientAuth
        from src.services.credential_auth import CredentialAuth
        from src.services.sign_auth import SignatureAuth

        # normalize input dict / pydantic model
        data = auth.dict() if hasattr(auth, "dict") else dict(auth)

        memberid = str(data.get("memberid", "")).strip()
        trxid = str(data.get("trxid", "")).strip()
        product = str(data.get("product", "")).strip()
        dest = str(data.get("dest", "")).strip()
        pin = data.get("pin")
        password = data.get("password")
        sign = data.get("sign")

        # 1) Client auth (IP check)
        ClientAuth(self.settings).validate(memberid, client_ip)

        has_pin_auth = pin is not None and password is not None
        has_sign_auth = sign is not None

        # 2) Credential / signature validation
        if has_pin_auth:
            CredentialAuth(self.settings).validate(memberid, pin, password)

            # generate expected sign using provided pin+password
            expected_sign = self.signature.generate_transaction_signature(
                memberid, product, dest, trxid, pin, password
            )

            if has_sign_auth and str(sign).upper() != expected_sign.upper():
                raise AuthError("signature tidak valid", 401)

            final_sign = expected_sign
        elif has_sign_auth:
            # verify signature using stored credentials
            SignatureAuth(self.signature).validate(
                memberid,
                product,
                dest,
                trxid,
                sign,
                pin=self.settings.OTO.pin,
                password=self.settings.OTO.password,
            )
            final_sign = sign
        else:
            raise AuthError("Provide either 'pin' and 'password', or 'sign'.", 400)

        return {
            "status": "success",
            "trxid": trxid,
            "memberid": memberid,
            "sign": final_sign,
        }
