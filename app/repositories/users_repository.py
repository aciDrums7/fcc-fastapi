""" Users Repository """
from sqlalchemy.orm import Session
from app.models.users_model import UserModel


# * GET


def get_users(db_session: Session, skip: int, limit: int) -> list[UserModel]:
    """Get Users"""
    db_users = (
        db_session.query(UserModel)
        .order_by(UserModel.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return db_users


def get_user_by_id(db_session: Session, user_id: int) -> UserModel | None:
    """Get User By Id"""
    db_user = db_session.query(UserModel).filter(UserModel.id == user_id).first()

    return db_user


def get_user_by_email(db_session: Session, user_email: str) -> UserModel | None:
    """Get User By Email"""
    db_user = db_session.query(UserModel).filter(UserModel.email == user_email).first()

    return db_user
