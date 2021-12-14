from pydantic import BaseSettings


class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    access_token_expire_minutes: int = 60
    refresh_token_expire_minutes: int = 60

    mongo_db_connection_string: str
    posts_collection: str
    mongo_db_indexes: str
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_INITDB_DATABASE: str

    class Config:
        case_sensitive = True
