"""Module ini menjelaskan model data untuk member dalam domain aplikasi.

actual di otomax itu memilki field lebih banyak.
"""

from pydantic import BaseModel, Field


class Member(BaseModel):
    """Definisi Minimal member model.

    actual di database itu menggunakan model dan properti lebih banyak.
    seperti nama nik allow no sign dan lain lain.

    Attributes:
        memberid (str): ini adalah id unik untuk member.
        balance (int): saldo member.
        pin (str): pin untuk autentikasi.
        password (str): password untuk autentikasi.
        ip_address (str): ip address terakhir member.
        report_url (str): url untuk laporan member.
        allow_nosign (bool): status mengizinkan tanpa signature saat request.
        is_active (bool): status aktif member.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel untuk validasi data.
    """

    memberid: str = Field(description="ID unik untuk member")
    balance: int = Field(
        default=0,
        description="Saldo member",
    )
    pin: str = Field(description="PIN untuk autentikasi")
    password: str = Field(description="Password untuk autentikasi")
    ip_address: str = Field(description="IP address terakhir member")
    report_url: str = Field(description="URL untuk laporan member")
    allow_nosign: bool = Field(
        default=False,
        description="Status mengizinkan tanpa signature saat request",
    )
    is_active: bool = Field(
        default=True,
        description="Status aktif member",
    )
