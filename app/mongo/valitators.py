from bson import ObjectId


def validate_mongo_id(values: dict):
    _id: ObjectId = values.get("_id", None)
    if _id is None or not ObjectId.is_valid(str(_id)):
        return None, None
    return str(_id), ObjectId(_id).generation_time
