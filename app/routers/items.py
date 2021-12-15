from fastapi import APIRouter, HTTPException, Depends
from typing import List
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.tortoise import paginate

from schemas.schemas import CategorySchema, TagSchema, PostViewSchema, PostCreateSchema
from models import User, Category, Tag, Post
from .common_query_params import CommonQueryParams
from security.auth import AuthUser
from security.header import api_key_header


router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.get("/post_list",
            response_model=Page[PostViewSchema],
            dependencies=(api_key_header,))
async def get_post_list(common: CommonQueryParams = Depends(CommonQueryParams),
                        params: Params = Depends(),
                        authorize: AuthUser = Depends()
                        ):
    condition_map = {'author_id': {'author_id': common.author_id},
                     'category_slug': {'category__slug': common.category_slug},
                     'tag_slug': {'tag__slug': common.tag_slug}
                     }
    await authorize.requires_access_token(required=False)
    queryset = Post.all().prefetch_related('category', 'tag', 'author')
    queryset = queryset if authorize.get_user_or_none() is not None else queryset.filter(logged_only=False)
    for key, value in condition_map.items():
        if getattr(common, key):
            return await paginate(queryset.filter(**value), params)
    return await paginate(queryset, params)


@router.get("/post/{post_id}", response_model=PostViewSchema)
async def get_the_user(post_id: int):
    post = await Post.get(id=post_id).prefetch_related('category', 'tag', 'author')
    return PostViewSchema.from_orm(post)


@router.get("/tag_list", response_model=List[TagSchema])
async def get_tags():
    query_set = await Tag.all()
    return [TagSchema.from_orm(model) for model in query_set]


@router.get("/category_list", response_model=List[CategorySchema])
async def get_categories():
    queryset = await Category.all()
    return [CategorySchema.from_orm(model) for model in queryset]


@router.post("/tag/create", response_model=TagSchema)
async def create_tag(tag: TagSchema):
    tag_obj = await Tag.create(**tag.dict(exclude_unset=True))
    return TagSchema.from_orm(tag_obj)


@router.post("/category/create", response_model=CategorySchema)
async def create_category(category: CategorySchema):
    category_obj = await Category.create(**category.dict(exclude_unset=True))
    return CategorySchema.from_orm(category_obj)


@router.post("/post/create", response_model=PostCreateSchema)
async def create_post(new_post: PostCreateSchema):
    user = await User.get(id=new_post.author_id)
    if user:
        post_obj = await Post.create(author=user, **new_post.dict())
        tags = await Tag.filter(id__in=new_post.tags_id)
        cats = await Category.filter(id__in=new_post.categories_id)
        await post_obj.tag.add(*tags)
        await post_obj.category.add(*cats)
        await post_obj.fetch_related('category', 'tag')
    else:
        raise HTTPException(status_code=404, detail='Id not Found')
