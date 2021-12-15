from math import ceil
from typing import Optional, List
from fastapi import APIRouter, Depends

from security.auth import AuthUser
from security.header import api_key_header

from mongo.mongo_crud import content_crud
from schemas.schemas_mongo import (PostCreateSchemaMongo, PostViewSchemaMongo,
                                   CommentCreateSchemaMongo, CommentListSchemaMongo,
                                   PostDetailViewSchemaMongo, TagListSchemaMongo,
                                   TagCreateSchemaMongo, CategoryCreateSchemaMongo, CategoryListSchemaMongo)

router = APIRouter(
    prefix="/mongo",
    tags=["mongo"],
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
    count = await content_crud.get_collection().count_documents({}) if logged \
        else await content_crud.get_collection().count_documents({'logged_only': False})
    pag = 0
    if (page and size) is not None:
        pag = 1
        skips = size * (page - 1)
        data = await content_crud.get_post_list(logged=logged, paginate=True, page_size=size, skips=skips)
    else:
        data = await content_crud.get_post_list(logged=logged)
    items = {
        "items": data,
        "total_docs": count,
        "page_size": size,
        "page_num": page,
        "total_pages": (ceil(count / size)) if pag else None
        }
    return items


@router.get("/post/{post_id}", response_description="Post Detail", response_model=List[PostDetailViewSchemaMongo])
async def post_detail_mongo(post_id: str):
    data = await content_crud.get_post(post_id=post_id)
    return data


@router.post("/add_comment", response_description="Add new comment", response_model=CommentCreateSchemaMongo)
async def new_comment(comment: CommentCreateSchemaMongo):
    await content_crud.add_comment(comment)
    return CommentCreateSchemaMongo.dict(comment)


@router.get("/comment_list", response_description="All comments", response_model=CommentListSchemaMongo)
async def comment_list():
    data = await content_crud.comment_list()
    items = {"comments": data}
    return items


@router.post("/add_tag", response_description="Add tag", response_model=TagCreateSchemaMongo)
async def add_tag(tag: TagCreateSchemaMongo):
    await content_crud.add_tag(tag)
    return CommentCreateSchemaMongo.dict(tag)


@router.get("/tag_list", response_description="All tags", response_model=TagListSchemaMongo)
async def tag_list():
    data = await content_crud.tag_list()
    items = {"tags": data}
    return items


@router.post("/add_category", response_description="Add category", response_model=CategoryCreateSchemaMongo)
async def add_category(category: CategoryCreateSchemaMongo):
    await content_crud.add_category(category)
    return CategoryCreateSchemaMongo.dict(category)


@router.get("/category_list", response_description="All categories", response_model=CategoryListSchemaMongo)
async def category_list():
    data = await content_crud.category_list()
    items = {"categories": data}
    return items

