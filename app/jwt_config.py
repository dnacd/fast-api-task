from pydantic import BaseModel
from functools import lru_cache

from config import Settings


@lru_cache()
def get_settings():
    return Settings()


class JWTSettings(BaseModel):
    authjwt_secret_key = get_settings().JWT_SECRET_KEY
    authjwt_access_token_expires = get_settings().access_token_expire_minutes
    authjwt_refresh_token_expires = get_settings().refresh_token_expire_minutes

