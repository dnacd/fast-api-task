from math import ceil
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import JSONResponse

from routers.common_query_params import CommonQueryParams
from security.auth import AuthUser
from security.header import api_key_header
from s3_events.s3_upload_file import upload_to_s3

from mongo.mongo_crud import content_crud
from schemas.mongo import *
from mongo.pg_mongo_aggregation import merge_user_data
from mongo.helpers import put_post_image

router = APIRouter(
    prefix="/mongo",
    tags=["mongo"],
    responses={404: {"description": "Not found"}},
)


@router.post("/new_post", response_description="Create new Post", response_model=ResponsePostCreateSchema)
async def create_post(post: RequestPostCreateSchema = Depends(),
                      file: UploadFile = File(..., description='uploading file')):
    data = await put_post_image(post, upload_to_s3(file))
    return data


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


@router.get("/post/{post_id}", response_description="Post Detail", response_model=ResponsePostSchema)
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


@router.put("/post/update/{post_id}", response_description="Post update")
async def post_update(post_id: str, post: RequestPostUpdateSchema):
    updated_post = await content_crud.update_post(post_id=post_id, update_data=dict(post))
    if updated_post is not None:
        return ResponseUpdatePostSchema(**updated_post)
    return HTTPException(status_code=404, detail=f'Post {post_id} Not Found')


@router.post("/add_comment", response_description="Add new comment", response_model=ResponseCommentSchema)
async def new_comment(comment: RequestCommentCreateSchema):
    data = await content_crud.add_comment(comment)
    return data


@router.get("/comment_list", response_description="All comments", response_model=ResponseCommentListSchema)
async def comment_list():
    data = await content_crud.comment_list()
    items = {"comments": data}
    return items


@router.post("/add_tag", response_description="Add tag", response_model=ResponseTagSchema)
async def add_tag(tag: RequestTagCreateSchema):
    data = await content_crud.add_tag(tag)
    return data


@router.get("/tag_list", response_description="All tags", response_model=ResponseTagListSchema)
async def tag_list():
    data = await content_crud.tag_list()
    items = {"tags": data}
    return items


@router.post("/add_category", response_description="Add category", response_model=ResponseCategorySchema)
async def add_category(category: RequestCategoryCreateSchema):
    data = await content_crud.add_category(category)
    return data


@router.get("/category_list", response_description="All categories", response_model=ResponseCategoryListSchema)
async def category_list():
    data = await content_crud.category_list()
    items = {"categories": data}
    return items
