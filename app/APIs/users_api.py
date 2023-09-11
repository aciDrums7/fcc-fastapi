""" Users APIs """

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.db_config import get_db
from app.schemas.users_schemas import UserOut, UserUpsert
from app.services import users_service
from app.exceptions.http_exceptions import (
    UnauthorizedException,
    ForbiddenException,
    NotFoundException,
    InternalServerErrorException,
)
from app.authentication import oauth2_service

router = APIRouter(prefix="/users", tags=["Users"])


# 5 GET


@router.get("", response_model=list[UserOut])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db_session: Session = Depends(get_db),
    # current_user: UserOut = Depends(oauth2_service.get_current_user),
):
    """Get Users"""
    try:
        users = users_service.get_users(db_session, skip, limit)
        return users

    except Exception as exc_500:
        print(exc_500)
        raise InternalServerErrorException(exc_500) from exc_500


@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id(
    user_id: int,
    db_session: Session = Depends(get_db),
    # current_user: UserOut = Depends(oauth2_service.get_current_user),
):
    """Get User By Id"""
    try:
        user = users_service.get_user_by_id(db_session, user_id)
        return user

    except NotFoundException as exc_404:
        print(exc_404)
        raise exc_404
    except Exception as exc_500:
        print(exc_500)
        raise InternalServerErrorException(exc_500) from exc_500


@router.get("/email/{user_email}", response_model=UserOut)
def get_user_by_email(
    user_email: str,
    db_session: Session = Depends(get_db),
    # current_user: UserOut = Depends(oauth2_service.get_current_user),
):
    """Get User By Email"""
    try:
        user = users_service.get_user_by_email(db_session, user_email)
        return user

    except NotFoundException as exc_404:
        print(exc_404)
        raise exc_404
    except Exception as exc_500:
        print(exc_500)
        raise InternalServerErrorException(exc_500) from exc_500


# 5 POST


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(
    user: UserUpsert,
    db_session: Session = Depends(get_db),
    # current_user: UserOut = Depends(oauth2_service.get_current_user),
):
    """Create a new User"""
    try:
        db_user = users_service.create_user(db_session, user)
        return db_user

    except Exception as exc_500:
        print(exc_500)
        raise InternalServerErrorException(exc_500) from exc_500


# 5 PUT


@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    user: UserUpsert,
    db_session: Session = Depends(get_db),
    current_user: UserOut = Depends(oauth2_service.get_current_user),
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
    except Exception as exc_500:
        print(exc_500)
        raise InternalServerErrorException(exc_500) from exc_500


# 5 DELETE


@router.delete(
    "/{user_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
def delete_user(
    user_id: int,
    db_session: Session = Depends(get_db),
    current_user: UserOut = Depends(oauth2_service.get_current_user),
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
    except Exception as exc_500:
        print(exc_500)
        raise InternalServerErrorException(exc_500) from exc_500
