import motor.motor_asyncio
from pymongo.database import Database as MongoDatabase
from functools import lru_cache

from config import Settings


@lru_cache()
def get_settings():
    return Settings()


class SingletonMeta(type):
    _instances = {}

    def call(cls, args, **kwargs):
        if cls not in cls._instances:
            instance = super().call(args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class MongoConnection(metaclass=SingletonMeta):
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(get_settings().mongo_db_connection_string)
        self.db: MongoDatabase = self.client[get_settings().MONGO_INITDB_DATABASE]
        self.create_mongo_indexes()

    def create_mongo_indexes(self) -> None:
        posts_collection = self.db.get_collection(get_settings().posts_collection)
        posts_collection.create_index(get_settings().mongo_db_indexes)


def get_mongo_db() -> MongoConnection:
    return MongoConnection()

