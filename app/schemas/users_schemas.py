""" Users Schemas """

from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """UserBase Class"""

    email: EmailStr
    password: str


class UserUpsert(UserBase):
    """UserUpsert Class"""


class User(UserBase):
    """User Class"""

    id: int
    created_at: datetime

    class Config:
        """SqlAlchemy Config Class"""

        from_attributes = True
