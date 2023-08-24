""" Votes Schemas"""

from pydantic import BaseModel, ConfigDict, conint


class VoteBase(BaseModel):
    """VoteBase Schema Class"""

    model_config = ConfigDict(from_attributes=True)

    post_id: int


class VotePayload(VoteBase):
    """VotePayload Schema Class"""

    dir: conint(ge=0, le=1)


class VoteOut(VoteBase):
    """VoteBase Schema Class"""

    user_id: int
