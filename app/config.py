from pydantic import BaseSettings


class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    access_token_expire_minutes: int = 60
    refresh_token_expire_minutes: int = 60

    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    S3_Bucket: str
    S3_Key: str

    mongo_db_connection_string: str
    posts_collection: str
    mongo_db_indexes: str
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_INITDB_DATABASE: str

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    class Config:
        case_sensitive = True
