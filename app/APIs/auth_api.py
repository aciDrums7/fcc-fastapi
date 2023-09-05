""" Auth APIs """
from fastapi import APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.db_config import get_db
from app.exceptions.http_exceptions import (
    InternalServerErrorException,
    UnauthorizedException,
)
from app.schemas.token_schemas import Token
from app.authentication import oauth2_service


router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("", response_model=Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db),
):
    """Login User"""
    try:
        token = oauth2_service.login_user(user_credentials, db_session)

        return token

    except UnauthorizedException as exc_401:
        print(exc_401)
        raise exc_401
    except InternalServerErrorException as exc_500:
        print(exc_500)
        raise exc_500
