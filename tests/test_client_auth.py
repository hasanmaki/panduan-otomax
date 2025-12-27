from src.config.settings import Settings, UserCred
from src.services.client_auth import ClientAuth
from src.services.errors import AuthError


def make_settings(enable_ip_check: bool = True) -> Settings:
    return Settings(
        OTO=UserCred(
            memberid="TESTOK01",
            password="TESTOK01",
            pin="1111",
            memberip="10.0.0.2:9000",
            memberreporturl="http://example/report",
            enable_ip_check=enable_ip_check,
        )
    )


def test_client_auth_rejects_invalid_ip():
    s = make_settings(enable_ip_check=True)
    ca = ClientAuth(s)

    try:
        ca.validate("TESTOK01", "1.2.3.4")
        raise AssertionError("Expected AuthError due to invalid IP")
    except AuthError as exc:
        assert exc.status_code == 403
        assert "invalid IP" in exc.detail


def test_client_auth_allows_when_disabled():
    s = make_settings(enable_ip_check=False)
    ca = ClientAuth(s)

    # should not raise
    ca.validate("TESTOK01", "9.9.9.9")
