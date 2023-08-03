""" Users APIs """

from fastapi import APIRouter, Depends, status
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas import users_schemas
from app.services import users_service
from app.exceptions.exception_handling import (
    NotFoundException,
    raise_not_found_exception,
    raise_internal_server_error,
)

router = APIRouter(prefix="/users", tags=["Users"])


""" GET """


@router.get("", response_model=list[users_schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get Users"""
    try:
        users = users_service.get_users(db, skip, limit)

        return users

    except Exception as err:
        raise_internal_server_error(err)


@router.get("/{user_id}", response_model=users_schemas.User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Get User By Id"""
    try:
        user = users_service.get_user_by_id(db, user_id)
        if user == None:
            raise NotFoundException

        return user

    except NotFoundException as err:
        raise_not_found_exception(err)
    except Exception as err:
        raise_internal_server_error(err)


# @router.get("/{user_email}", response_model=users_schemas.User)
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


@router.post("", status_code=status.HTTP_201_CREATED, response_model=users_schemas.User)
def create_user(user: users_schemas.UserUpsert, db: Session = Depends(get_db)):
    """Create a new User"""
    try:
        db_user = users_service.create_user(db, user)

        return db_user

    except Exception as err:
        raise_internal_server_error(err)


""" PUT """


@router.put("/{user_id}")
def update_user(
    user_id: int, user: users_schemas.UserUpsert, db: Session = Depends(get_db)
):
    """Update a User"""
    try:
        db_user = users_service.get_user_by_email(db, user_id)
        if db_user is None:
            raise NotFoundException
        updated_user = users_service.update_user(db, user_id, user)

        return updated_user

    except NotFoundException as err:
        raise_not_found_exception(err)
    except Exception as err:
        raise_internal_server_error(err)


""" DELETE """


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a User"""
    try:
        deleted_user = users_service.delete_user(db, user_id)
        if deleted_user is None:
            raise NotFoundException

        return None

    except NotFoundException as err:
        raise_not_found_exception(err)
    except Exception as err:
        raise_internal_server_error(err, user_id)
