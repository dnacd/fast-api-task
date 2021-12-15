from math import ceil
from typing import Optional
from fastapi import APIRouter, Body, Depends
from security.auth import AuthUser
from security.header import api_key_header

from mongo.mongo_crud import content_crud
from schemas import PostCreateSchemaMongo, PostViewSchemaMongo

router = APIRouter(
    prefix="/mongo",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.post("/new_post", response_description="Create new Post", response_model=PostCreateSchemaMongo)
async def create_post(post: PostCreateSchemaMongo):
    await content_crud.new_post(post)
    return PostCreateSchemaMongo.dict(post)


@router.get("/post_list",
            response_description="List of posts",
            dependencies=(api_key_header,),
            response_model=PostViewSchemaMongo)
async def post_list_mongo(page: Optional[int] = None,
                          size: Optional[int] = None,
                          authorize: AuthUser = Depends()):
    await authorize.requires_access_token(required=False)
    logged = True if authorize.get_user_or_none() is not None else None
    if (page and size) is not None:
        skips = size * (page - 1)
        count = await content_crud.get_collection().count_documents({}) if logged \
            else await content_crud.get_collection().count_documents({'logged_only': False})
        data = await content_crud.get_post_list(logged=logged, paginate=True, page_size=size, skips=skips)
        items = {
            "items": data,
            "page_size": size,
            "page_num": page,
            "total_pages": ceil(count / size),
            "total_docs": count
        }
        return items
    else:
        data = await content_crud.get_post_list(logged=logged)
        return data


@router.get("/post/{post_id}", response_description="Post Detail", response_model=PostCreateSchemaMongo)
async def post_detail_mongo(post_id: str):
    data = await content_crud.get_post(post_id=post_id)
    return data