from pydantic.class_validators import root_validator
from pydantic.main import BaseModel

from .valitators import validate_mongo_id


class PostIdMixin(BaseModel):
    @root_validator(pre=True)
    def validate_id(cls, values):
        post_id, created = validate_mongo_id(values)
        if "post_id" not in values:
            values["post_id"] = post_id
        if "created" not in values:
            values["created"] = created
        return values
