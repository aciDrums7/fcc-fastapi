""" Auth APIs """
from fastapi import APIRouter, Depends
from app.database import get_db
from sqlalchemy.orm import Session
from app.exceptions.exception_handling import (
    InvalidCredentialsException,
    raise_invalid_credentials,
    raise_internal_server_error,
)
from app.schemas import users_schemas
from app.services import users_service
from app.utils.hashing import verify

router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("")
def login(user_credentials: users_schemas.UserLogin, db: Session = Depends(get_db)):
    """Create a new User"""
    try:
        db_user = users_service.get_user_by_email(db, user_credentials.email)
        if not db_user or not verify(user_credentials.password, db_user.password):
            raise InvalidCredentialsException

        return db_user

    except InvalidCredentialsException as err:
        raise_invalid_credentials(err)
    except Exception as err:
        raise_internal_server_error(err)
