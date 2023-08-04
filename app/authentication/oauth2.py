from jose import JWTError, jwt
from datetime import datetime, timedelta

# 1 SECRET KEY
# 2 ALGORITHM
# 3 EXPIRATION TIME

SECRET_KEY = "a3b02165d4a2c1909714d816c1f1c9df7e17ebfc274cc7dd4e43cb7b7ee4bd28"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 37


def create_access_token(payload: dict) -> str:
    to_encode = payload.copy()
    expire_time = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expiration": str(expire_time)})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
