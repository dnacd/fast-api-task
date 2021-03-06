from typing import List, Optional

from pymongo.collection import Collection
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from functools import lru_cache

from config import Settings
from mongo.db_mongo import get_mongo_db
from .aggregations import make_aggregation

from schemas.mongo import *

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
        return mongo_db.db.get_collection(get_settings().posts_collection)

    async def new_post(self, post: PostCreateDBSchema) -> ResponsePostSchema:
        post = jsonable_encoder(post)
        data = await self.get_collection().insert_one(post)
        created_post = await self.get_collection().find_one({"_id": ObjectId(data.inserted_id)})
        return created_post

    async def get_post_list(self, logged=False,
                            paginate=False,
                            page_size=None,
                            skips=None,
                            filter_match=None) -> List[ResponsePostSchema]:
        keyword_args = {
            "logged": logged,
            "paginate": paginate,
            "page_size": page_size,
            "skips": skips,
            "match_value": filter_match}
        data = await self.get_collection().aggregate(make_aggregation(**keyword_args)).to_list(10000)
        return [ResponsePostSchema(**one) for one in data]

    async def update_post(self, post_id: str, update_data: dict) -> ResponseUpdatePostSchema:
        await self.get_collection().update_one({'_id': ObjectId(post_id)}, {'$set': update_data})
        find = await self.get_collection().find_one({"_id": ObjectId(post_id)})
        return find

    async def get_post(self, post_id: str) -> Optional[ResponsePostSchema]:
        finder = {"$match": {"_id": ObjectId(post_id)}}
        data = await self.get_collection().aggregate(make_aggregation(finder=finder)).to_list(1)
        if data:
            return ResponsePostSchema(**data[0])
        return None

    async def delete_post(self, post_id: str):
        finder = {"_id": ObjectId(post_id)}
        data = await self.get_collection().delete_one(finder)
        return data

    async def add_comment(self, comment: CommentCreateDBSchema) -> ResponseCommentSchema:
        comment = jsonable_encoder(comment)
        data = await self.get_collection_by_name('comments').insert_one(comment)
        created_comment = await self.get_collection_by_name('comments').find_one({"_id": ObjectId(data.inserted_id)})
        return created_comment

    async def comment_list(self) -> ResponseCommentListSchema:
        data = await self.get_collection_by_name('comments').find().to_list(10000)
        return data

    async def add_tag(self, tag: TagCreateDBSchema):
        tag = jsonable_encoder(tag)
        data = await self.get_collection_by_name('tags').insert_one(tag)
        created_tag = await self.get_collection_by_name('tags').find_one({"_id": ObjectId(data.inserted_id)})
        return created_tag

    async def tag_list(self) -> ResponseTagListSchema:
        data = await self.get_collection_by_name('tags').find().to_list(10000)
        return data

    async def add_category(self, category: CategoryCreateDBSchema):
        category = jsonable_encoder(category)
        data = await self.get_collection_by_name('categories').insert_one(category)
        created_category = await self.get_collection_by_name('categories').find_one({"_id": ObjectId(data.inserted_id)})
        return created_category

    async def category_list(self):
        data = await self.get_collection_by_name('categories').find().to_list(10000)
        return data


content_crud = ContentCRUD()
