from bson import ObjectId
from pydantic import BaseModel
from typing import List


from mongo.valitators import PyObjectId
from pydantic.fields import Field


class CommentCreateSchema(BaseModel):
    id: PyObjectId = Field(default_factory=ObjectId, alias='_id')
    post_id: str
    user_id: int
    text: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "post_id": "mongo_obj_id",
                "user_id": 1,
                "text": "ContentString",
            }
        }


class CommentViewSchema(BaseModel):
    post_id: str
    user_id: int
    text: str


class CommentListSchemaMongo(BaseModel):
    comments: List[CommentViewSchema]
