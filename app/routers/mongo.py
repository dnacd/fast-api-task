from typing import List, Optional
from fastapi import APIRouter, Body


from mongo.mongo_crud import content_crud
from schemas import PostCreateSchemaMongo


router = APIRouter(
    prefix="/mongo",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.post("/new_post", response_description="Create new Post", response_model=PostCreateSchemaMongo)
async def create_post(post: PostCreateSchemaMongo = Body(...)):
    await content_crud.new_post(post)
    return PostCreateSchemaMongo.dict(post)


@router.get("/post_list", response_description="List of posts", response_model=List[PostCreateSchemaMongo])
async def post_list_mongo(page: Optional[int] = None, size: Optional[int] = None):
    if page and size is not None:
        data = await content_crud.get_post_list(page_num=page, page_size=size)
    else:
        data = await content_crud.get_post_list(page_num=page, page_size=size, sizable=False)
    return [post for post in data]


@router.post("/post/{post_id}", response_description="Post Detail", response_model=PostCreateSchemaMongo)
async def post_detail_mongo(post_id: str):
    data = await content_crud.get_post(post_id=post_id)
    return data
