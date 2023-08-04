""" Users APIs """

from typing import Union
from fastapi import APIRouter, Depends, status
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.schemas.users_schemas import User, UserUpsert
from app.schemas.token_schemas import TokenData
from app.services import users_service
from app.exceptions.http_exceptions import (
    NotFoundException,
    InternalServerErrorException,
)
from app.authentication import oauth2

router = APIRouter(prefix="/users", tags=["Users"])


""" GET """


@router.get("", response_model=list[User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get Users"""
    try:
        users = users_service.get_users(db, skip, limit)

        return users

    except Exception as err:
        raise InternalServerErrorException(err)


@router.get("/{user_id}", response_model=Union[User, None])
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Get User By Id"""
    try:
        user = users_service.get_user_by_id(db, user_id)
        if not user:
            raise NotFoundException(f"User with id: {user_id} not found")

        return user

    except NotFoundException as err:
        print(err)
        raise err
    except Exception as err:
        raise InternalServerErrorException(err)


# @router.get("/{user_email}", response_model=User)
# def get_user_by_id(user_email: str, db: Session = Depends(get_db)):
#     """Get User By Email"""
#     try:
#         user = users_service.get_user_by_email(db, user_email)
#         if user == None:
#             raise NotFoundException

#         return user

#     except NotFoundException as err:
#         raise_not_found_exception(err)
#     except Exception as err:
#         raise_internal_server_error(err)


""" POST """


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Union[User, None])
def create_user(
    user: UserUpsert,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(oauth2.get_current_user),
):
    """Create a new User"""
    try:
        db_user = users_service.create_user(db, user)

        return db_user

    except Exception as err:
        raise InternalServerErrorException(err)


""" PUT """


@router.put("/{user_id}", response_model=Union[User, None])
def update_user(
    user_id: int,
    user: UserUpsert,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(oauth2.get_current_user),
):
    """Update a User"""
    try:
        db_user = users_service.get_user_by_id(db, user_id)
        if not db_user:
            raise NotFoundException(f"User with id: {user_id} not found")

        updated_user = users_service.update_user(db, user_id, user)
        return updated_user

    except NotFoundException as err:
        print(err)
        raise err
    except Exception as err:
        raise InternalServerErrorException(err)


""" DELETE """


@router.delete(
    "/{user_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(oauth2.get_current_user),
):
    """Delete a User"""
    try:
        deleted_user = users_service.delete_user(db, user_id)
        if not deleted_user:
            raise NotFoundException(f"User with id: {user_id} not found")

        return None

    except NotFoundException as err:
        print(err)
        raise err
    except Exception as err:
        raise InternalServerErrorException(err)
