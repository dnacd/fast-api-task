import datetime
from bson import ObjectId
from pydantic import BaseModel, constr, HttpUrl
from typing import Optional, List
from mongo.valitators import PyObjectId

from pydantic.fields import Field
from mongo.mixins import PostIdMixin


class PostCreateSchema(BaseModel):
    id: PyObjectId = Field(default_factory=ObjectId, alias='_id')
    author_id: int
    title: constr(max_length=80)
    slug: constr(max_length=35)
    categories_id: List[str]
    tags_id: List[str]
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
                "slug": "slugfield",
                "categories_id": ["ObjectId", "ObjectId"],
                "tags_id": ["ObjectId", "ObjectId"],
                "content": "ContentString",
                "image": "https://exampleimage.com/image.png",
                "logged_only": False
            }
        }


class CatTagJoinSchema(BaseModel):
    title: str
    slug: str


class ViewListUserSchema(BaseModel):
    id: int
    username: constr(max_length=24)

    class Config:
        orm_mode = True


class UserInAggregationSchema(BaseModel):
    username: constr(max_length=24)


class CommentsJoinSchema(BaseModel):
    user_id: int
    username: Optional[str]
    text: str


class PostSchema(PostIdMixin):
    post_id: str
    author_id: int
    author: Optional[UserInAggregationSchema]
    title: constr(max_length=55)
    slug: constr(max_length=35)
    image: HttpUrl
    created: datetime.datetime
    logged_only: bool
    comments: List[CommentsJoinSchema]
    categories: List[CatTagJoinSchema]
    tags: List[CatTagJoinSchema]


class PostViewSchema(BaseModel):
    items: List[PostSchema]
    page_size: Optional[int]
    page_num: Optional[int]
    total_pages: Optional[int]
    total_docs: Optional[int]


class PostUpdateSchema(BaseModel):
    title: constr(max_length=80)
    slug: constr(max_length=35)
    categories_id: List[str]
    tags_id: List[str]
    content: str
    image: HttpUrl
    logged_only: bool

    class Config:
        schema_extra = {
            "example": {
                "title": "Title",
                "slug": "slugfield",
                "categories_id": ["ObjectId", "ObjectId"],
                "tags_id": ["ObjectId", "ObjectId"],
                "content": "ContentString",
                "image": "https://exampleimage.com/image.png",
                "logged_only": False
            }
        }


class ResponseUpdatePostSchema(PostIdMixin):
    post_id: str
    author_id: int
    title: constr(max_length=55)
    slug: constr(max_length=35)
    image: HttpUrl
    created: datetime.datetime
    logged_only: bool
    categories_id: List
    tags_id: List
