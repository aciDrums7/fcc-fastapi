from typing import Union
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.exceptions.http_exceptions import UnauthorizedException
from app.models.users_model import User
from app.schemas.token_schemas import TokenData
from app.services import users_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "a3b02165d4a2c1909714d816c1f1c9df7e17ebfc274cc7dd4e43cb7b7ee4bd28"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 37


def create_access_token(payload: dict) -> str:
    to_encode = payload.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    #! Don't change "exp" key!
    # ? jwt.decode() will check the "exp" claim to see if the token is expired!
    to_encode.update({"exp": expire_time})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_jwt(token: str) -> Union[TokenData, None]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: str = payload.get("user_id")
        if not user_id:
            return None
        token_data = TokenData(id=user_id)

        return token_data
    except JWTError as err:
        print(err)
        raise UnauthorizedException(err)


def get_current_user(token: TokenData = Depends(oauth2_scheme)) -> Union[User, None]:
    current_user = users_service.get_user_by_id(token.id)
    return current_user
