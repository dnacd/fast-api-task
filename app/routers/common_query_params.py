from typing import Optional


class CommonQueryParams:
    def __init__(self,
                 author_id: Optional[int] = None,
                 category_slug: Optional[str] = None,
                 tag_slug: Optional[str] = None,
                 ):
        self.author_id = author_id
        self.category_slug = category_slug
        self.tag_slug = tag_slug
