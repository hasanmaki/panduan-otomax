# [ ] TODO : document this module bro
from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class UserCred(BaseModel):
    """user credential settings.

    Fields:
        - memberid: member identifier
        - password: shared password
        - pin: member pin
        - memberip: allowed member IP (optionally with port)
        - memberreporturl: callback/report URL
        - enable_ip_check: toggle IP validation (env: OTO_ENABLE_IP_CHECK)
    """

    memberid: str
    password: str
    pin: str
    memberip: str
    memberreporturl: str
    enable_ip_check: bool = True

    model_config = {"extra": "forbid"}


class Settings(BaseSettings):
    """application settings from environment variables."""

    OTO: UserCred

    model_config = {
        "env_file": ".env",
        "env_nested_delimiter": "_",
        "extra": "ignore",
    }


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()  # type: ignore
