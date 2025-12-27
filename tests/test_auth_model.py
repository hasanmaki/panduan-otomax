import pytest
from src.api.api_trx import Auth


def test_auth_model_trims_and_accepts_pin_password():
    a = Auth(
        trxid=" trx1 ",
        memberid=" mid ",
        product=" prod ",
        dest=" dst ",
        pin=" 1234 ",
        password=" secret ",
    )
    assert a.trxid == "trx1"
    assert a.memberid == "mid"
    assert a.pin == "1234"
    assert a.password == "secret"


def test_auth_model_accepts_sign_only():
    a = Auth(trxid="trx2", memberid="mid", product="prod", dest="dst", sign=" abc ")
    assert a.sign == "abc"


def test_auth_model_requires_one_of_pin_or_sign():
    with pytest.raises(ValueError):
        Auth(trxid="trx3", memberid="mid", product="prod", dest="dst")
