""" Users Schemas """

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    """UserBase Schema Class"""

    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    password: str
    phone_number: Optional[str] = None


class UserUpsert(UserBase):
    """UserUpsert Schema Class"""


class UserOut(UserBase):
    """UserOut Schema Class"""

    id: int
    created_at: datetime
