""" Auth APIs """
from typing import Union
from fastapi import APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.exceptions.http_exceptions import (
    InternalServerErrorException,
    UnauthorizedException,
)
from app.schemas.token_schemas import Token
from app.services import users_service
from app.utils.hashing import verify
from app.authentication import oauth2


router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("", response_model=Union[Token, None])
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Create a new User"""
    try:
        # ? OAuth2PasswordRequestForm username = email in our case
        db_user = users_service.get_user_by_email(db, user_credentials.username)
        if not db_user or not verify(user_credentials.password, db_user.password):
            raise UnauthorizedException("Invalid user credentials")

        jwt = oauth2.create_access_token({"user_id": db_user.id})

        return Token(access_token=jwt, token_type="Bearer")

    # TODO: fix exception handling!
    except UnauthorizedException as err:
        print(err)
        raise err
    except Exception as err:
        print(err)
        raise InternalServerErrorException(err)
