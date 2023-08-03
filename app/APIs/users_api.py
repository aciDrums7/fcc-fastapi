""" Users APIs """

from fastapi import APIRouter, Depends, status
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import users_schemas
from ..services import users_service
from ..exceptions import exception_handling
from ..exceptions.exception_handling import NotFoundException

router = APIRouter()

""" GET """


@router.get("", response_model=list[users_schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get Users"""
    try:
        users = users_service.get_users(db, skip, limit)

        return users

    except Exception as err:
        exception_handling.raise_internal_server_error(err)


@router.get("/{user_id}", response_model=users_schemas.User)
def get_post(user_id: int, db: Session = Depends(get_db)):
    """Get User"""
    try:
        user = users_service.get_user(db, user_id)
        if user == None:
            raise NotFoundException

        return user

    except NotFoundException as err:
        exception_handling.raise_not_found_exception(err, user_id)
    except Exception as err:
        exception_handling.raise_internal_server_error(err)


""" POST """


@router.post("", status_code=status.HTTP_201_CREATED, response_model=users_schemas.User)
def create_post(user: users_schemas.UserUpsert, db: Session = Depends(get_db)):
    """Create a new User"""
    try:
        db_user = users_service.create_user(db, user)

        return db_user

    except Exception as err:
        exception_handling.raise_internal_server_error(err)


""" PUT """


@router.put("/{user_id}")
def update_post(
    user_id: int, user: users_schemas.UserUpsert, db: Session = Depends(get_db)
):
    """Update a User"""
    try:
        db_user = users_service.get_user(db, user_id)
        if db_user is None:
            raise NotFoundException
        updated_user = users_service.update_user(db, user_id, user)

        return updated_user

    except NotFoundException as err:
        exception_handling.raise_not_found_exception(err, user_id)
    except Exception as err:
        exception_handling.raise_internal_server_error(err)


""" DELETE """


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(user_id: int, db: Session = Depends(get_db)):
    """Delete a User"""
    try:
        deleted_user = users_service.delete_user(db, user_id)
        if deleted_user is None:
            raise NotFoundException

        return None

    except NotFoundException as err:
        exception_handling.raise_not_found_exception(err, user_id)
    except Exception as err:
        exception_handling.raise_internal_server_error(err, user_id)
