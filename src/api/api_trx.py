from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel

from src.config.settings import get_settings
from src.services.auth import AuthenticationService, AuthError
from src.services.siganture_auth import OtomaxSignatureService

router = APIRouter(tags=["Transaction"])

"""pydantic schema for handling trx request and response."""


class Auth(BaseModel):
    """transaksi requirement with either pin/password atau signature."""

    trxid: str
    memberid: str
    dest: str
    product: str
    pin: str | None = None
    password: str | None = None
    sign: str | None = None

    model_config = {"extra": "forbid", "str_strip_whitespace": True}


@router.get("/trx")
async def get_trx(auth: Annotated[Auth, Query()], request: Request):
    """Endpoint transaksi. Semua logika auth didelegasikan ke service."""
    auth_service = AuthenticationService(OtomaxSignatureService, get_settings())
    try:
        result = auth_service.authenticate_transaction(auth, request.client.host)
    except AuthError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)
    return result
