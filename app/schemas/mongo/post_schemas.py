import datetime
from bson import ObjectId
from pydantic import BaseModel, constr, HttpUrl
from typing import Optional, List

from mongo.mixins import PostIdMixin


class RequestPostCreateSchema(BaseModel):
    author_id: int
    title: constr(max_length=80)
    slug: constr(max_length=35)
    categories_id: List[str]
    tags_id: List[str]
    content: str
    logged_only: bool

    class Config:
        schema_extra = {
            "example": {
                "author_id": 1,
                "title": "Title",
                "slug": "slugfield",
                "categories_id": ["ObjectId", "ObjectId"],
                "tags_id": ["ObjectId", "ObjectId"],
                "content": "ContentString",
                "logged_only": False
            }
        }


class PostCreateDBSchema(PostIdMixin):
    post_id: str
    author_id: int
    title: constr(max_length=80)
    slug: constr(max_length=35)
    categories_id: List[str]
    tags_id: List[str]
    content: str
    image: Optional[HttpUrl]
    logged_only: bool
    resize_process: bool
    sizes: Optional[List]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ResponsePostCreateSchema(PostIdMixin):
    post_id: str
    author_id: int
    title: constr(max_length=80)
    slug: constr(max_length=35)
    categories_id: List[str]
    tags_id: List[str]
    content: str
    image: HttpUrl
    logged_only: bool
    resize_process: bool
    sizes: Optional[List]


class CatTagJoinSchema(BaseModel):
    title: str
    slug: str


class ResponseUserSchema(BaseModel):
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


class ResponsePostSchema(PostIdMixin):
    post_id: str
    author_id: int
    author: Optional[UserInAggregationSchema]
    title: constr(max_length=55)
    slug: constr(max_length=35)
    image: Optional[HttpUrl]
    created: datetime.datetime
    logged_only: bool
    comments: List[CommentsJoinSchema]
    categories: List[CatTagJoinSchema]
    tags: List[CatTagJoinSchema]
    resize_process: bool
    sizes: Optional[List]


class PostViewSchema(BaseModel):
    items: List[ResponsePostSchema]
    page_size: Optional[int]
    page_num: Optional[int]
    total_pages: Optional[int]
    total_docs: Optional[int]


class RequestPostUpdateSchema(BaseModel):
    title: constr(max_length=80)
    slug: constr(max_length=35)
    categories_id: List[str]
    tags_id: List[str]
    content: str
    image: HttpUrl
    logged_only: bool
    resize_process: bool
    sizes: Optional[List]

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
    image: Optional[HttpUrl]
    tags_id: List
    resize_process: bool
    sizes: Optional[List]
