import datetime

from pydantic import BaseModel, constr, HttpUrl, validator, Field
from typing import Optional, List

from pydantic.networks import EmailStr


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
    password: Optional[str]

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

