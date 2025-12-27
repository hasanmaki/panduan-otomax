from src.config.settings import Settings, UserCred
from src.services.credential_auth import CredentialAuth
from src.services.errors import AuthError


def make_settings() -> Settings:
    return Settings(
        OTO=UserCred(
            memberid="TESTOK01",
            password="TESTOK01",
            pin="1111",
            memberip="10.0.0.2:9000",
            memberreporturl="http://example/report",
            enable_ip_check=True,
        )
    )


def test_credential_auth_accepts_valid():
    s = make_settings()
    ca = CredentialAuth(s)
    # should not raise
    ca.validate("TESTOK01", "1111", "TESTOK01")


def test_credential_auth_rejects_invalid():
    s = make_settings()
    ca = CredentialAuth(s)
    try:
        ca.validate("TESTOK01", "bad", "wrong")
        raise AssertionError("Expected AuthError for bad credentials")
    except AuthError as exc:
        assert exc.status_code == 401
        assert "pin password salah" in exc.detail
