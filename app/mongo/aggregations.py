def make_aggregation(logged=None, match_value=None, paginate=None, page_size=None, skips=None):
    aggregation = [{
        "$lookup": {
            "from": "comments",
            "localField": "_id",
            "foreignField": "post_id",
            "as": "comments",
        }
    },
        {
            "$lookup": {
                "from": "tags",
                "localField": "tags_id",
                "foreignField": "_id",
                "as": "tags",
            }
        },
        {
            "$lookup": {
                "from": "categories",
                "localField": "categories_id",
                "foreignField": "_id",
                "as": "categories",
            }
        }]
    if logged is None:
        aggregation.append({"$match": {'logged_only': False}})
    if match_value:
        aggregation.append(match_value)
    if paginate:
        aggregation.extend([{"$skip": skips}, {"$limit": page_size}])
    return aggregation
