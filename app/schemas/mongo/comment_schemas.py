from typing import List

from bson import ObjectId
from pydantic import BaseModel

from mongo.mixins import CommentsIdMixin


class RequestCommentCreateSchema(BaseModel):
    post_id: str
    user_id: int
    text: str

    class Config:
        schema_extra = {
            "example": {
                "post_id": "mongo_obj_id",
                "user_id": 1,
                "text": "ContentString",
            }
        }


class CommentCreateDBSchema(CommentsIdMixin):
    comment_id: str
    post_id: str
    user_id: int
    text: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ResponseCommentSchema(CommentsIdMixin):
    comment_id: str
    post_id: str
    user_id: int
    text: str


class ResponseCommentListSchema(BaseModel):
    comments: List[ResponseCommentSchema]
