from fastapi import APIRouter
from schemas.schemas import UserCreateSchema, ViewListUserSchema, UserInfoSchema
from typing import List
from models import User

from security.simple_hash import password_hash

router = APIRouter(
    prefix="/user",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.get("/list", response_model=List[ViewListUserSchema])
async def get_users() -> List:
    queryset = await User.all()
    return [ViewListUserSchema.from_orm(model) for model in queryset]


@router.get("/{user_id}", status_code=200, response_model=UserInfoSchema)
async def get_the_user(user_id: int):
    user = await User.get(id=user_id)
    return UserInfoSchema.from_orm(user)


@router.post("/signup", response_model=UserCreateSchema)
async def create_user(user: UserCreateSchema):
    user = await User.create(
                        username=user.username,
                        password_hash=password_hash(user.password),
                        email=user.email,
    )
    return UserCreateSchema.from_orm(user)
