""" Auth APIs """
from fastapi import APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.exceptions.exception_handling import (
    InvalidCredentialsException,
    raise_invalid_credentials,
    raise_internal_server_error,
)
from app.schemas import users_schemas
from app.services import users_service
from app.utils.hashing import verify
from app.authentication.oauth2 import create_access_token

router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("")
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Create a new User"""
    try:
        #? OAuth2PasswordRequestForm username = email in our case
        db_user = users_service.get_user_by_email(db, user_credentials.username)
        if not db_user or not verify(user_credentials.password, db_user.password):
            raise InvalidCredentialsException

        jwt = create_access_token({"user_id": db_user.id})

        return {"access_token": jwt, "token_type": "bearer"}

    except Exception as err:
        raise_internal_server_error(err)
    except InvalidCredentialsException as err:
        raise_invalid_credentials(err)
