from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    access_token_expire_minutes: int = 60
    refresh_token_expire_minutes: int = 60

    class Config:
        case_sensitive = True
