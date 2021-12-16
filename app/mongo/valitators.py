from bson import ObjectId


def validate_mongo_id(values: dict):
    _id: ObjectId = values.get("_id", None)
    if _id is None or not ObjectId.is_valid(str(_id)):
        return None, None
    return str(_id), ObjectId(_id).generation_time


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")
