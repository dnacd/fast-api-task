from bson import ObjectId
from pydantic import BaseModel
from typing import List
from mongo.mixins import CategoryIdMixin

from pydantic.fields import Field


class RequestCategoryCreateSchema(BaseModel):
    title: str
    slug: str

    class Config:
        schema_extra = {
            "example": {
                "title": "title",
                "slug": "slug",
            }
        }


class CategoryCreateDBSchema(CategoryIdMixin):
    category_id: str
    title: str
    slug: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ResponseCategorySchema(CategoryIdMixin):
    category_id: str
    title: str
    slug: str


class ResponseCategoryListSchema(BaseModel):
    categories: List[ResponseCategorySchema]
