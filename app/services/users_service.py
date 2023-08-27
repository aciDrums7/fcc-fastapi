""" Users Service """
from sqlalchemy.orm import Session
from app.repositories import users_repository
from app.models.users_model import UserModel
from app.schemas.users_schemas import UserOut, UserUpsert
from app.exceptions.http_exceptions import (
    ForbiddenException,
    NotFoundException,
)
from app.utils.password_utils import hash_password


# * GET


def get_users(db_session: Session, skip: int, limit: int) -> list[UserOut]:
    """Get Users"""
    db_users = users_repository.get_users(db_session, skip, limit)

    return [UserOut.model_validate(user) for user in db_users]


def get_user_by_id(db_session: Session, user_id: int) -> UserOut:
    """Get User By Id"""
    db_user = users_repository.get_user_by_id(db_session, user_id)

    if not db_user:
        raise NotFoundException(f"User with id: {user_id} not found")

    return UserOut.model_validate(db_user)


def get_user_by_email(db_session: Session, user_email: str) -> UserOut:
    """Get User By Email"""
    db_user = users_repository.get_user_by_email(db_session, user_email)

    if not db_user:
        raise NotFoundException("No Users found")

    return UserOut.model_validate(db_user)


# * POST


def create_user(
    db_session: Session,
    user: UserUpsert,
    # current_user: UserOut,
) -> UserOut:
    """Create User"""
    # TODO: if current_user.role == 'ADMIN'
    # if current_user:
    # 1 hash the password
    user.password = hash_password(user.password)

    # 2 persist the user in the database
    db_user = UserModel(**user.model_dump())
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)

    return UserOut.model_validate(db_user)


# * PUT


def update_user(
    db_session: Session,
    user_id: int,
    user_updated: UserUpsert,
    current_user: UserOut,
) -> UserOut:
    """Update User"""
    db_user = users_repository.get_user_by_id(db_session, user_id)

    if not db_user:
        raise NotFoundException(f"User with id: {db_user} not found")
    if db_user.id != current_user.id:
        raise ForbiddenException("Not authorized to perform requested action")

    for attr, value in user_updated.model_dump(exclude_unset=True).items():
        if attr == "password":
            setattr(db_user, attr, hash_password(value))
            continue
        setattr(db_user, attr, value)

    db_session.commit()
    db_session.refresh(db_user)

    return UserOut.model_validate(db_user)


# * DELETE


def delete_user(
    db_session: Session,
    user_id: int,
    current_user: UserOut,
) -> None:
    """Delete User"""
    db_user = users_repository.get_user_by_id(db_session, user_id)

    if not db_user:
        raise NotFoundException(f"User with id: {user_id} not found")
    if db_user.id != current_user.id:
        raise ForbiddenException("Not authorized to perform requested action")

    db_session.delete(db_user)
    db_session.commit()

    return None
