from typing import List
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


@router.post("/post_list", response_description="List of posts", response_model=List[PostCreateSchemaMongo])
async def post_list_mongo():
    data = await content_crud.get_post_list()
    return [post for post in data]


@router.post("/post/{post_id}", response_description="Post Detail", response_model=PostCreateSchemaMongo)
async def post_detail_mongo(post_id: str):
    data = await content_crud.get_post(post_id=post_id)
    return data