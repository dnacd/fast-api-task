from mongo.mongo_crud import content_crud
from schemas.mongo import ResponsePostSchema


async def put_post_image(post, file=None) -> ResponsePostSchema:
    post = ResponsePostSchema.dict(post)
    post['image'] = file
    post['sizes'] = []
    post['resize_process'] = False
    data = await content_crud.new_post(post)
    return data
