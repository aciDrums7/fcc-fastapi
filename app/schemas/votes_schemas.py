""" Votes Schemas"""

from pydantic import BaseModel, conint


class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)
