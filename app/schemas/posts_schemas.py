""" Posts Schemas """
# ? pydantic is useful for data validation (request body/params) + schema definition
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from .users_schemas import UserOut


class PostBase(BaseModel):
    """PostBase Schema Class"""

    model_config = ConfigDict(from_attributes=True)

    title: str = None
    content: str = None
    # 1 if not provided, default value will be False
    published: Optional[bool] = False
    # 2 optional value, if not provided, default value will be None
    rating: Optional[int] = None


class PostUpsert(PostBase):
    """PostUpsert Schema Class"""


class PostOut(PostBase):
    """PostOut Schema Class"""

    id: int
    created_at: datetime
    # owner_id: int
    owner: UserOut
    # ? Needed to be excluded when converted to SqlAlchemy PostModel
    n_votes: int = 0
