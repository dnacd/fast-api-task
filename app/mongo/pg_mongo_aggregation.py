from models import User
from schemas.mongo.post_schemas import ViewListUserSchema


async def merge_user_data(data, single=False):
    users = [ViewListUserSchema.from_orm(user) for user in await User.all()]
    users_dict = {user.id: user for user in users}
    if not single:
        for post in data:
            post.author = users_dict.get(post.author_id)
            for comment in post.comments:
                if users_dict.get(comment.user_id):
                    comment.username = users_dict.get(comment.user_id).username
    else:
        data.author = users_dict.get(data.author_id)
        for comment in data.comments:
            if users_dict.get(comment.user_id):
                comment.username = users_dict.get(comment.user_id).username
    return data
