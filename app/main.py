from fastapi import FastAPI

from postgres.db_postgres import init_db
from routers import items, users, api, mongo
from fastapi_jwt_auth import AuthJWT
from jwt_config import JWTSettings


def create_application() -> FastAPI:
    application = FastAPI()
    return application


app = create_application()
app.include_router(items.router)
app.include_router(users.router)
app.include_router(api.router)
app.include_router(mongo.router)
init_db(app)


@AuthJWT.load_config
def get_jwt_config():
    return JWTSettings()
