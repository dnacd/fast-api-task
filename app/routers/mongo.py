from math import ceil
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from routers.common_query_params import CommonQueryParams
from security.auth import AuthUser
from security.header import api_key_header

from mongo.mongo_crud import content_crud
from schemas.mongo.category_schemas import CategoryCreateSchemaMongo, CategoryListSchemaMongo
from schemas.mongo.comment_schemas import CommentCreateSchemaMongo, CommentListSchemaMongo
from schemas.mongo.post_detail_schemas import PostDetailViewSchemaMongo
from schemas.mongo.post_schemas import PostCreateSchemaMongo, PostViewSchemaMongo
from schemas.mongo.tags_schemas import TagCreateSchemaMongo, TagListSchemaMongo

router = APIRouter(
    prefix="/mongo",
    tags=["mongo"],
    responses={404: {"description": "Not found"}},
)


@router.post("/new_post", response_description="Create new Post", response_model=PostCreateSchemaMongo)
async def create_post(post: PostCreateSchemaMongo):
    await content_crud.new_post(post)
    return PostCreateSchemaMongo.dict(post)


@router.get("/post_list", response_description="List of posts", dependencies=(api_key_header,),
            response_model=PostViewSchemaMongo)
async def post_list_mongo(page: Optional[int] = None,
                          size: Optional[int] = None,
                          authorize: AuthUser = Depends(),
                          common: CommonQueryParams = Depends(CommonQueryParams)):

    await authorize.requires_access_token(required=False)
    condition_map = {'category_slug': {"$match": {"categories": {"$elemMatch": {"slug": common.category_slug}}}},
                     'tag_slug': {"$match": {"tags": {"$elemMatch": {"slug": common.tag_slug}}}},
                     'author_id': {"$match": {"author_id": common.author_id}}
                     }
    filter_value = None
    for key, value in condition_map.items():
        if getattr(common, key):
            filter_value = value
    logged = True if authorize.get_user_or_none() is not None else None
    count = await content_crud.get_collection().count_documents({}) if logged \
        else await content_crud.get_collection().count_documents({'logged_only': False})
    keyword_args = {
        "logged": logged,
        "paginate": True if (page and size) else None,
        "page_size": size,
        "skips": size * (page - 1) if size else None,
        "filter_match": filter_value
    }
    data = await content_crud.get_post_list(**keyword_args)
    items = {
        "items": data,
        "total_docs": count,
        "page_size": size,
        "page_num": page,
        "total_pages": (ceil(count / size)) if size else None
    }
    return items


@router.get("/post/{post_id}", response_description="Post Detail", response_model=List[PostDetailViewSchemaMongo])
async def post_detail_mongo(post_id: str):
    data = await content_crud.get_post(post_id=post_id)
    return data


@router.delete("/post/delete/{id}", response_description="Delete a student")
async def delete_post(post_id: str):
    delete_result = await content_crud.delete_post(post_id)
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Student {post_id} not found")


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
