from pymongo.collection import Collection
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from functools import lru_cache
from math import ceil

from config import Settings
from mongo.db_mongo import get_mongo_db

mongo_db = get_mongo_db()


@lru_cache()
def get_settings():
    return Settings()


class ContentCRUD:
    @staticmethod
    def get_collection_by_name(collection_name) -> Collection:
        return mongo_db.db.get_collection(collection_name)

    @staticmethod
    def get_collection() -> Collection:
        """
        Get main collection for Post documents
        :return: Collection
        """
        return mongo_db.db.get_collection(get_settings().posts_collection)

    async def new_post(self, post):
        post = jsonable_encoder(post)
        data = await self.get_collection().insert_one(post)
        created_post = await self.get_collection().find_one({"_id": data.inserted_id})
        return created_post

    async def get_post_list(self, page_size, page_num, logged=False):
        unlogged = await self.get_collection().find({'logged_only': False}).to_list(10000)
        if (page_size and page_num) is not None:
            skips = page_size * (page_num - 1)
            data = await self.get_collection().find().skip(skips).limit(page_size).to_list(10000) if logged \
                else unlogged
            count = await self.get_collection().count_documents({}) if logged \
                else await self.get_collection().count_documents({'logged_only': False})
            items = {
                "items": data,
                "page_size": page_size,
                "page_num": page_num,
                "total_pages": ceil(count / page_size),
                "total_docs": count
            }
            return items
        else:
            return await self.get_collection().find().to_list(10000) if logged else unlogged

    async def update_post(self, post_id: str, update_data: dict):
        result = await self.get_collection().update_one({'_id': ObjectId(post_id)}, {'$set': update_data})
        return result

    async def get_post(self, post_id: str):
        if (post := await self.get_collection().find_one({"_id": post_id})) is not None:
            return post


content_crud = ContentCRUD()
