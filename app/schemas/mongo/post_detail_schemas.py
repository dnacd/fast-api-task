from pydantic import BaseModel, constr, HttpUrl
from typing import List

from mongo.mixins import PostIdMixin


class TagsJoinSchemaMongo(BaseModel):
    title: str
    slug: str


class CategoriesJoinSchemaMongo(BaseModel):
    title: str
    slug: str


class CommentsJoinSchemaMongo(BaseModel):
    user_id: int
    text: str


class PostDetailViewSchemaMongo(PostIdMixin):
    post_id: str
    author_id: int
    title: constr(max_length=55)
    slug: constr(max_length=35)
    image: HttpUrl
    logged_only: bool
    comments: List[CommentsJoinSchemaMongo]
    tags: List[TagsJoinSchemaMongo]
    categories: List[CategoriesJoinSchemaMongo]
