from src.services.siganture_auth import OtomaxSignatureService
from src.services.sign_auth import SignatureAuth


def test_signature_auth_accepts_correct_signature():
    svc = SignatureAuth(OtomaxSignatureService)
    data = dict(
        memberid="M1", product="P1", dest="081", refid="R1", pin="111", password="pwd"
    )
    sig = OtomaxSignatureService.generate_transaction_signature(**data)

    # should not raise
    svc.validate(
        data["memberid"],
        data["product"],
        data["dest"],
        data["refid"],
        sig,
        pin=data["pin"],
        password=data["password"],
    )


def test_signature_auth_rejects_bad_signature():
    svc = SignatureAuth(OtomaxSignatureService)
    data = dict(
        memberid="M1", product="P1", dest="081", refid="R1", pin="111", password="pwd"
    )
    sig = OtomaxSignatureService.generate_transaction_signature(**data)

    try:
        svc.validate(
            data["memberid"],
            data["product"],
            data["dest"],
            data["refid"],
            "bad-sig",
            pin=data["pin"],
            password=data["password"],
        )
        raise AssertionError("Expected AuthError for bad signature")
    except Exception as exc:
        assert getattr(exc, "status_code", 401) == 401
