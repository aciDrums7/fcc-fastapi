""" Auth APIs """
from typing import Union
from fastapi import APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.db_config import get_db_session
from app.exceptions.http_exceptions import (
    InternalServerErrorException,
    UnauthorizedException,
)
from app.schemas.token_schemas import Token
from app.authentication import oauth2_service


router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("", response_model=Union[Token, None])
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db_session),
):
    """Login User"""
    try:
        token = oauth2_service.login_user(user_credentials, db_session)

        return token

    except UnauthorizedException as exc_403:
        print(exc_403)
        raise exc_403
    except InternalServerErrorException as exc_500:
        print(exc_500)
        raise exc_500
