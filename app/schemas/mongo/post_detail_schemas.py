from pydantic import BaseModel, constr, HttpUrl
from typing import List

from mongo.mixins import PostIdMixin
from .post_schemas import CatTagJoinSchema


class CommentsJoinSchema(BaseModel):
    user_id: int
    text: str


class PostDetailViewSchema(PostIdMixin):
    post_id: str
    author_id: int
    author: str
    title: constr(max_length=55)
    slug: constr(max_length=35)
    image: HttpUrl
    logged_only: bool
    comments: List[CommentsJoinSchema]
    tags: List[CatTagJoinSchema]
    categories: List[CatTagJoinSchema]
