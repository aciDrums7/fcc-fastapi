""" Users APIs """

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.db_config import get_db_session
from app.schemas.users_schemas import User, UserUpsert
from app.services import users_service
from app.exceptions.http_exceptions import (
    UnauthorizedException,
    ForbiddenException,
    NotFoundException,
    InternalServerErrorException,
)
from app.authentication import oauth2_service

router = APIRouter(prefix="/users", tags=["Users"])


# * GET


@router.get("", response_model=list[User])
def get_users(
    skip: int = 0, limit: int = 100, db_session: Session = Depends(get_db_session)
):
    """Get Users"""
    try:
        users = users_service.get_users(db_session, skip, limit)
        return users

    except InternalServerErrorException as exc_500:
        print(exc_500)
        raise exc_500


@router.get("/{user_id}", response_model=User)
def get_user_by_id(user_id: int, db_session: Session = Depends(get_db_session)):
    """Get User By Id"""
    try:
        user = users_service.get_user_by_id(db_session, user_id)
        return user

    except NotFoundException as exc_404:
        print(exc_404)
        raise exc_404
    except InternalServerErrorException as exc_500:
        print(exc_500)
        raise exc_500


# * POST


@router.post("", status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(
    user: UserUpsert,
    db_session: Session = Depends(get_db_session),
    current_user: User = Depends(oauth2_service.get_current_user),
):
    """Create a new User"""
    try:
        db_user = users_service.create_user(db_session, user, current_user)
        return db_user

    except InternalServerErrorException as exc_500:
        print(exc_500)
        raise exc_500


# * PUT


@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user: UserUpsert,
    db_session: Session = Depends(get_db_session),
    current_user: User = Depends(oauth2_service.get_current_user),
):
    """Update a User"""
    try:
        updated_user = users_service.update_user(
            db_session, user_id, user, current_user
        )
        return updated_user

    except UnauthorizedException as exc_401:
        print(exc_401)
        raise exc_401
    except NotFoundException as exc_404:
        print(exc_404)
        raise exc_404
    except ForbiddenException as exc_403:
        print(exc_403)
        raise exc_403
    except InternalServerErrorException as exc_500:
        print(exc_500)
        raise exc_500


# * DELETE


@router.delete(
    "/{user_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
def delete_user(
    user_id: int,
    db_session: Session = Depends(get_db_session),
    current_user: User = Depends(oauth2_service.get_current_user),
):
    """Delete a User"""
    try:
        users_service.delete_user(db_session, user_id, current_user)
        return None

    except UnauthorizedException as exc_401:
        print(exc_401)
        raise exc_401
    except NotFoundException as exc_404:
        print(exc_404)
        raise exc_404
    except ForbiddenException as exc_403:
        print(exc_403)
        raise exc_403
    except InternalServerErrorException as exc_500:
        print(exc_500)
        raise exc_500
