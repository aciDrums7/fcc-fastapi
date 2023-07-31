""" Schemas File """
# ? pydantic is useful for data validation (request body/params) + schema definition
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PostBase(BaseModel):
    """Class PostBase"""

    title: str = None
    content: str = None
    # 1 if not provided, default value will be False
    published: Optional[bool] = False
    # 2 optional value, if not provided, default value will be None
    rating: Optional[int] = None
    created_at: Optional[datetime] = None


class PostUpsert(PostBase):
    pass


class Post(PostBase):
    id: int

    # ? Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict
    # ? but an ORM model (or any other arbitrary object with attributes).
    class Config:
        #! orm_mode DEPRECATED
        from_attributes = True
