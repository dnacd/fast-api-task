from bson import ObjectId
from pydantic import BaseModel
from typing import List

from mongo.mixins import TagIdMixin


class RequestTagCreateSchema(BaseModel):
    title: str
    slug: str

    class Config:
        schema_extra = {
            "example": {
                "title": "title",
                "slug": "slug",
            }
        }


class TagCreateDBSchema(TagIdMixin):
    tag_id: str
    title: str
    slug: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ResponseTagSchema(TagIdMixin):
    tag_id: str
    title: str
    slug: str


class ResponseTagListSchema(BaseModel):
    tags: List[ResponseTagSchema]
