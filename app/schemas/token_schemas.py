""" Token Schemas """

from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """Token Class"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """TokenData Class"""

    id: Optional[int] = None
