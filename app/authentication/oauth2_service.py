""" OAuth2 Authentication Service"""
from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database.db_config import get_db_session
from app.exceptions.http_exceptions import UnauthorizedException
from app.models.users_model import User
from app.schemas.token_schemas import Token, TokenData
from app.services import users_service
from app.utils.password_utils import verify_password
from app.utils.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(payload: dict) -> str:
    """Create a new access token"""
    to_encode = payload.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    #! Don't change "exp" key!
    # ? jwt.decode() will check the "exp" claim to see if the token is expired!
    to_encode.update({"exp": expire_time})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_jwt(token: str) -> TokenData:
    """Verifies if the given token is valid"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: str = payload.get("user_id")
        if not user_id:
            return None
        token_data = TokenData(id=user_id)

        return token_data
    except JWTError as err:
        print(err)
        raise UnauthorizedException(err) from err


def get_current_user(
    token: str = Depends(oauth2_scheme), db_session: Session = Depends(get_db_session)
) -> User:
    """Get current logged in user"""
    token_data = verify_jwt(token)
    current_user = users_service.get_user_by_id(db_session, token_data.id)
    return current_user


def login_user(
    user_credentials: OAuth2PasswordRequestForm, db_session: Session
) -> Token:
    """Verifies if user can login and eventually returns a new token"""
    # ? OAuth2PasswordRequestForm username = email in our case
    db_user = users_service.get_user_by_email(db_session, user_credentials.username)
    is_password_valid = verify_password(user_credentials.password, db_user.password)

    if not db_user or not is_password_valid:
        raise UnauthorizedException("Invalid user credentials")

    token = create_access_token({"user_id": db_user.id})

    return Token(access_token=token, token_type="Bearer")
