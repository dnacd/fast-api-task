from models import User
from schemas.mongo.post_schemas import ResponseUserSchema


def merge_helper(data, users_dict):
    data.author = users_dict.get(data.author_id)
    for comment in data.comments:
        if users_dict.get(comment.user_id):
            comment.username = users_dict.get(comment.user_id).username


async def merge_user_data(data, single=False):
    users = [ResponseUserSchema.from_orm(user) for user in await User.all()]
    users_dict = {user.id: user for user in users}
    if single:
        merge_helper(data, users_dict)
        return data
    for post in data:
        merge_helper(post, users_dict)
    return data
