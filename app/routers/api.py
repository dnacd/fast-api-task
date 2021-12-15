from fastapi import APIRouter, Depends

from models import User
from security.auth import AuthUser
from security.header import api_key_header
from schemas import UserLoginSchema, UserInfoSchema
from security.simple_hash import password_hash

router = APIRouter(
    prefix="",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/settings/profile",
    response_model=UserInfoSchema,
    operation_id="get_user_profile",
    dependencies=(api_key_header,)
)
async def get_profile_settings(
        authorize: AuthUser = Depends(),
):
    """
    Returns profile details of current authorized user
    \f
    :param authorize:
    :return:
    """
    await authorize.requires_access_token()
    return UserInfoSchema.from_orm(authorize.get_user())


@router.post("/login")
async def get_access_token(user_from_db: UserLoginSchema,
                           authorize: AuthUser = Depends()):
    user = await User.get_or_none(email=user_from_db.email)
    if user is not None and user.password_hash == password_hash(user_from_db.password):
        authorize.user = user
        await authorize.get_user()
        return authorize.create_tokens()
    else:
        return 'BAD LOGIN OR PASSWORD'


