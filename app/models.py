""" Models File """
from sqlalchemy import Boolean, Column, DateTime, Integer, String, func

from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=True, default=False)
    rating = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=func.now())
