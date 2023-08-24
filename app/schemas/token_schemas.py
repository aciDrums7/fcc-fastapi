""" Token Schemas """

from typing import Optional
from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    """Token Class"""

    model_config = ConfigDict(from_attributes=True)

    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """TokenData Schema Class"""

    user_id: Optional[int] = None
