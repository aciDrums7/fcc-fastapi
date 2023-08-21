""" Posts Model """
from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    text,
)
from sqlalchemy.orm import relationship
from app.database.db_config import Base


class Post(Base):
    """Post Table Class"""

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=True, default=False)
    rating = Column(Integer, nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    owner = relationship("User")
