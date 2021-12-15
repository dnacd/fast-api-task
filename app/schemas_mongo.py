import datetime
from bson import ObjectId
from pydantic import BaseModel, constr, HttpUrl
from typing import Optional, List
from mongo.pyobj_id import PyObjectId

from pydantic.fields import Field
from mongo.mixins import PostIdMixin


class PostCreateSchemaMongo(BaseModel):
    id: PyObjectId = Field(default_factory=ObjectId, alias='_id')
    author_id: int
    title: constr(max_length=55)
    slug: constr(max_length=35)
    content: str
    image: HttpUrl
    logged_only: bool

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "author_id": 1,
                "title": "Title",
                "slug": "Slug",
                "content": "ContentString",
                "image": "https://exampleimage.com/image.png",
                "logged_only": False
            }
        }


class PostSchemaMongo(PostIdMixin):
    post_id: str
    author_id: int
    title: constr(max_length=55)
    slug: constr(max_length=35)
    image: HttpUrl
    created: datetime.datetime
    logged_only: bool


class PostViewSchemaMongo(BaseModel):
    items: List[PostSchemaMongo]
    page_size: Optional[int]
    page_num: Optional[int]
    total_pages: Optional[int]
    total_docs: Optional[int]


class PostDetailViewSchemaMongo(PostIdMixin):
    post_id: str
    author_id: int
    title: constr(max_length=55)
    slug: constr(max_length=35)
    image: HttpUrl
    logged_only: bool
    comments: List


class CommentCreateSchemaMongo(BaseModel):
    id: PyObjectId = Field(default_factory=ObjectId, alias='_id')
    post_id: str
    user_id: int
    text: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "post_id": "mongo_obj_id",
                "user_id": 1,
                "text": "ContentString",
            }
        }


class CommentViewSchemaMongo(BaseModel):
    post_id: str
    user_id: int
    text: str


class CommentListSchemaMongo(BaseModel):
    comments: List[CommentViewSchemaMongo]
