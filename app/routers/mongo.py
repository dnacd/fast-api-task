from math import ceil
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from models import User
from routers.common_query_params import CommonQueryParams
from security.auth import AuthUser
from security.header import api_key_header

from mongo.mongo_crud import content_crud
from schemas.mongo.category_schemas import CategoryCreateSchema, CategoryListSchema
from schemas.mongo.comment_schemas import CommentCreateSchema, CommentListSchemaMongo
from schemas.mongo.post_detail_schemas import PostDetailViewSchema
from schemas.mongo.post_schemas import PostCreateSchema, PostViewSchema, PostUpdateSchema, \
    ResponseUpdatePostSchema, ViewListUserSchema, PostSchema
from schemas.mongo.tags_schemas import TagCreateSchema, TagListSchema
from mongo.pg_mongo_aggregation import merge_user_data

router = APIRouter(
    prefix="/mongo",
    tags=["mongo"],
    responses={404: {"description": "Not found"}},
)


@router.post("/new_post", response_description="Create new Post", response_model=PostCreateSchema)
async def create_post(post: PostCreateSchema):
    await content_crud.new_post(post)
    return PostCreateSchema.dict(post)


@router.get("/post_list", response_description="List of posts", dependencies=(api_key_header,),
            response_model=PostViewSchema)
async def post_list_mongo(page: Optional[int] = None,  size: Optional[int] = None, authorize: AuthUser = Depends(),
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
    count_documents = await content_crud.get_collection().count_documents({}) if logged \
        else await content_crud.get_collection().count_documents({'logged_only': False})
    keyword_args = {
        "logged": logged,
        "paginate": True if (page and size) else None,
        "page_size": size,
        "skips": size * (page - 1) if size else None,
        "filter_match": filter_value
    }
    data = await content_crud.get_post_list(**keyword_args)
    await merge_user_data(data)
    items = {
        "items": data,
        "total_docs": count_documents,
        "page_size": size,
        "page_num": page,
        "total_pages": (ceil(count_documents / size)) if size else None
    }
    return items


@router.get("/post/{post_id}", response_description="Post Detail", response_model=PostSchema)
async def post_detail_mongo(post_id: str):
    data = await content_crud.get_post(post_id=post_id)
    await merge_user_data(data, single=True)
    return data


@router.delete("/post/delete/{post_id}", response_description="Delete a student")
async def delete_post(post_id: str):
    delete_result = await content_crud.delete_post(post_id)
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Post {post_id} not found")


@router.put("/post/update/{post_id}", response_description="Post update", response_model=ResponseUpdatePostSchema)
async def post_update(post_id: str, post: PostUpdateSchema):
    updated_post = await content_crud.get_collection().update_one({"_id": post_id}, {"$set": post.dict()})
    post_body = await content_crud.get_collection().find_one({"_id": post_id})
    if updated_post:
        return post_body


@router.post("/add_comment", response_description="Add new comment", response_model=CommentCreateSchema)
async def new_comment(comment: CommentCreateSchema):
    await content_crud.add_comment(comment)
    return CommentCreateSchema.dict(comment)


@router.get("/comment_list", response_description="All comments", response_model=CommentListSchemaMongo)
async def comment_list():
    data = await content_crud.comment_list()
    items = {"comments": data}
    return items


@router.post("/add_tag", response_description="Add tag", response_model=TagCreateSchema)
async def add_tag(tag: TagCreateSchema):
    await content_crud.add_tag(tag)
    return CommentCreateSchema.dict(tag)


@router.get("/tag_list", response_description="All tags", response_model=TagListSchema)
async def tag_list():
    data = await content_crud.tag_list()
    items = {"tags": data}
    return items


@router.post("/add_category", response_description="Add category", response_model=CategoryCreateSchema)
async def add_category(category: CategoryCreateSchema):
    await content_crud.add_category(category)
    return CategoryCreateSchema.dict(category)


@router.get("/category_list", response_description="All categories", response_model=CategoryListSchema)
async def category_list():
    data = await content_crud.category_list()
    items = {"categories": data}
    return items
