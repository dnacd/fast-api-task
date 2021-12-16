from bson import ObjectId
from pydantic import BaseModel
from typing import List
from mongo.valitators import PyObjectId

from pydantic.fields import Field


class CategoryCreateSchemaMongo(BaseModel):
    id: PyObjectId = Field(default_factory=ObjectId, alias='_id')
    title: str
    slug: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "title",
                "slug": "slug",
            }
        }


class CategoryDetailSchemaMongo(BaseModel):
    id: str = Field(alias='_id')
    title: str
    slug: str


class CategoryListSchemaMongo(BaseModel):
    categories: List[CategoryDetailSchemaMongo]
