from mongo.mongo_crud import content_crud


async def put_post_image(post, file=None):
    post.image = file
    data = await content_crud.new_post(post)
    return data
