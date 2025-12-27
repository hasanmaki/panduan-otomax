from src.config.settings import Settings, UserCred
from src.services.auth import AuthenticationService, AuthError
from src.services.siganture_auth import OtomaxSignatureService


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


def test_ip_check_enabled_rejects_invalid_ip():
    settings = make_settings(enable_ip_check=True)
    svc = AuthenticationService(OtomaxSignatureService, settings)

    auth = {
        "trxid": "trx-1",
        "memberid": "TESTOK01",
        "product": "PROD",
        "dest": "08123456789",
        "pin": "1111",
        "password": "TESTOK01",
    }

    try:
        svc.authenticate_transaction(auth, client_ip="1.2.3.4")
        raise AssertionError("Expected AuthError due to invalid IP")
    except AuthError as exc:
        assert exc.status_code == 403
        assert "invalid IP" in exc.detail


def test_ip_check_disabled_allows_any_ip():
    settings = make_settings(enable_ip_check=False)
    svc = AuthenticationService(OtomaxSignatureService, settings)

    auth = {
        "trxid": "trx-2",
        "memberid": "TESTOK01",
        "product": "PROD",
        "dest": "08123456789",
        "pin": "1111",
        "password": "TESTOK01",
    }

    result = svc.authenticate_transaction(auth, client_ip="9.9.9.9")
    assert result["status"] == "success"
    assert result["trxid"] == "trx-2"


def test_pin_password_mismatch_raises():
    settings = make_settings(enable_ip_check=False)
    svc = AuthenticationService(OtomaxSignatureService, settings)

    auth = {
        "trxid": "trx-3",
        "memberid": "TESTOK01",
        "product": "PROD",
        "dest": "08123456789",
        "pin": "badpin",
        "password": "wrong",
    }

    try:
        svc.authenticate_transaction(auth, client_ip="9.9.9.9")
        raise AssertionError("Expected AuthError due to bad credentials")
    except AuthError as exc:
        assert exc.status_code == 401
        assert "pin password salah" in exc.detail


def test_sign_only_verification_with_stored_credentials():
    settings = make_settings(enable_ip_check=False)
    svc = AuthenticationService(OtomaxSignatureService, settings)

    auth_input = {
        "trxid": "trx-4",
        "memberid": "TESTOK01",
        "product": "PROD",
        "dest": "08123456789",
    }

    # generate signature using stored pin/password in settings
    expected_sign = OtomaxSignatureService.generate_transaction_signature(
        auth_input["memberid"],
        auth_input["product"],
        auth_input["dest"],
        auth_input["trxid"],
        settings.OTO.pin,
        settings.OTO.password,
    )

    auth = {**auth_input, "sign": expected_sign}

    result = svc.authenticate_transaction(auth, client_ip="9.9.9.9")
    assert result["status"] == "success"
    assert result["sign"] == expected_sign
