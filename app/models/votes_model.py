""" Votes Model """
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
)
from app.database.db_config import Base


class VoteModel(Base):
    """Votes Table Class"""

    __tablename__ = "votes"

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
