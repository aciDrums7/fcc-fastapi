""" Users Service """
from sqlalchemy.orm import Session
from app.models import users_model
from app.schemas import users_schemas
from app.exceptions.http_exceptions import (
    InternalServerErrorException,
    ForbiddenException,
    NotFoundException,
)
from app.utils.password_utils import hash_password


# * GET


def get_users(
    db_session: Session, skip: int = 0, limit: int = 100
) -> list[users_schemas.User]:
    """Get Users"""
    try:
        return (
            db_session.query(users_model.User)
            .order_by(users_model.User.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    except Exception as err:
        raise InternalServerErrorException(err) from err


def get_user_by_id(db_session: Session, user_id: int) -> users_schemas.User:
    """Get User By Id"""
    try:
        db_user = (
            db_session.query(users_model.User)
            .filter(users_model.User.id == user_id)
            .first()
        )
        if not db_user:
            raise NotFoundException(f"User with id: {user_id} not found")

        return db_user

    except Exception as err:
        raise InternalServerErrorException(err) from err


def get_user_by_email(db_session: Session, user_email: str) -> users_schemas.User:
    """Get User By Email"""
    try:
        db_user = (
            db_session.query(users_model.User)
            .filter(users_model.User.email == user_email)
            .first()
        )
        if not db_user:
            raise NotFoundException("No Users found")

        return db_user

    except Exception as err:
        raise InternalServerErrorException(err) from err


# * POST


def create_user(
    db_session: Session,
    user: users_schemas.UserUpsert,
    current_user: users_schemas.User,
) -> users_schemas.User:
    """Create User"""
    try:
        # TODO: if current_user.role == 'ADMIN'
        if current_user:
            # 1 hash the password
            user.password = hash_password(user.password)

            # 2 persist the user in the database
            db_user = users_model.User(**user.model_dump())
            db_session.add(db_user)
            db_session.commit()
            db_session.refresh(db_user)

            return db_user

    except Exception as err:
        raise InternalServerErrorException(err) from err


# * PUT


def update_user(
    db_session: Session,
    user_id: int,
    user: users_schemas.UserUpsert,
    current_user: users_schemas.User,
) -> users_schemas.User:
    """Update User"""
    try:
        db_user = get_user_by_id(db_session, user_id)

        if not db_user:
            raise NotFoundException(f"User with id: {db_user} not found")
        if db_user.owner_id != current_user.id:
            raise ForbiddenException("Not authorized to perform requested action")

        for attr, value in user.model_dump(exclude_unset=True).items():
            if attr == "password":
                setattr(db_user, attr, hash_password(value))
                continue
            setattr(db_user, attr, value)

        db_session.commit()
        db_session.refresh(db_user)

        return db_user

    except Exception as err:
        raise InternalServerErrorException(err) from err


# * DELETE


def delete_user(
    db_session: Session,
    user_id: int,
    current_user: users_schemas.User,
) -> users_schemas.User:
    """Delete User"""
    try:
        db_user = get_user_by_id(db_session, user_id)

        if not db_user:
            raise NotFoundException(f"User with id: {user_id} not found")
        if db_user.owner_id != current_user.id:
            raise ForbiddenException("Not authorized to perform requested action")

        db_session.delete(db_user)
        db_session.commit()

        return db_user

    except Exception as err:
        raise InternalServerErrorException(err) from err
