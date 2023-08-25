""" Users Model """
from sqlalchemy import TIMESTAMP, Column, Integer, String, text

from app.database.db_config import Base


class UserModel(Base):
    """User Table Class"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    phone_number = Column(String, nullable=True)
