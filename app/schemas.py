import datetime
from bson import ObjectId
from pydantic import BaseModel, constr, HttpUrl, validator
from typing import Optional, List
from mongo.pyobj_id import PyObjectId

from pydantic.fields import Field
from pydantic.networks import EmailStr
from mongo.mixins import PostIdMixin


class UserCreateSchema(BaseModel):
    username: constr(max_length=24)
    password: Optional[str]
    email: EmailStr

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": 'test',
                "email": "test@example.com",
                "password": "test"
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "test@example.com",
                "password": "test"
            }
        }


class UserInfoSchema(BaseModel):
    username: constr(max_length=24)
    password: Optional[str]
    email: EmailStr
    created_at: datetime.datetime
    modified_at: datetime.datetime

    class Config:
        orm_mode = True


class Tokens(BaseModel):
    """Refresh and access token pair"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ViewListUserSchema(BaseModel):
    username: constr(max_length=24)
    email: constr(max_length=60)

    class Config:
        orm_mode = True


class TagSchema(BaseModel):
    name: constr(max_length=48)
    slug: constr(max_length=50)

    class Config:
        orm_mode = True


class CategorySchema(BaseModel):
    name: constr(max_length=48)
    slug: constr(max_length=50)

    class Config:
        orm_mode = True


class PostCreateSchema(BaseModel):
    author_id: int
    title: constr(max_length=55)
    slug: constr(max_length=35)
    categories_id: List[int]
    tags_id: List[int]
    content: str
    image: HttpUrl
    logged_only: bool

    class Config:
        orm_mode = True


class UserName(BaseModel):
    username: str

    class Config:
        orm_mode = True


class PostViewSchema(BaseModel):
    author: UserName
    title: constr(max_length=55)
    slug: constr(max_length=35)
    category: List[CategorySchema]
    tag: List[TagSchema]
    content: constr(max_length=150)
    image: HttpUrl
    logged_only: bool

    @validator('category', 'tag', pre=True)
    def validator_m2m(cls, m2m):
        return [one for one in m2m]

    @validator('author', pre=True)
    def validator_author(cls, author):
        return author

    class Config:
        orm_mode = True


# Mongo schemas

class PostCreateSchemaMongo(BaseModel):
    id: PyObjectId = Field(default_factory=ObjectId, alias='_id')
    author_id: int
    title: constr(max_length=55)
    slug: constr(max_length=35)
    categories_id: List[int]
    tags_id: List[int]
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
                "title": "This is title",
                "slug": "This is slug",
                "categories_id": [1, 2, 3],
                "tags_id": [1, 2, 3],
                "content": "This is content string",
                "image": "https://exampleimage.com/image.png",
                "logged_only": False
            }
        }


class PostSchemaMongo(PostIdMixin):
    post_id: Optional[str]
    author_id: int
    title: constr(max_length=55)
    slug: constr(max_length=35)
    categories_id: List[int]
    tags_id: List[int]
    image: HttpUrl
    created: datetime.datetime
    logged_only: bool


class PostViewSchemaMongo(BaseModel):
    items: List[PostSchemaMongo]
    page_size: int
    page_num: int
    total_pages: int
    total_docs: int
