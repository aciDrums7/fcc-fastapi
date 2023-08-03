""" Users Service """
from typing import Optional
from sqlalchemy.orm import Session
from app.models import users_model
from app.schemas import users_schemas
from app.utils.hashing import hash


""" GET """


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[users_schemas.User]:
    """Get Users"""
    return (
        db.query(users_model.User)
        .order_by(users_model.User.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_user_by_id(db: Session, user_id: int) -> Optional[users_schemas.User]:
    """Get User By Id"""
    return db.query(users_model.User).filter(users_model.User.id == user_id).first()


def get_user_by_email(db: Session, user_email: str) -> Optional[users_schemas.User]:
    """Get User By Email"""
    return (
        db.query(users_model.User).filter(users_model.User.email == user_email).first()
    )


""" UPSERT """


def create_user(
    db: Session, user: users_schemas.UserUpsert
) -> Optional[users_schemas.User]:
    """Create User"""
    # 1 hash the password
    user.password = hash(user.password)

    # 2 persist the user in the database
    db_user = users_model.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user(
    db: Session, user_id: int, user: users_schemas.UserUpsert
) -> Optional[users_schemas.User]:
    """Update User"""
    db_user = get_user_by_id(db, user_id)
    if db_user is None:
        return None
    for attr, value in user.model_dump(exclude_unset=True).items():
        if attr == "password":
            setattr(db_user, attr, hash(value))
            continue
        setattr(db_user, attr, value)
    db.commit()
    db.refresh(db_user)

    return db_user


""" DELETE """


def delete_user(db: Session, user_id: int) -> Optional[users_schemas.User]:
    """Delete a post"""
    db_user = get_user_by_id(db, user_id)
    if db_user is None:
        return None
    db.delete(db_user)
    db.commit()

    return db_user
