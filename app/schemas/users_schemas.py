""" Users Schemas """

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    passwords: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserUpsert(UserBase):
    pass
