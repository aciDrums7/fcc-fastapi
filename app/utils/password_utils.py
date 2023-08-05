""" Hashing Utils """
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Returns an hashed password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: bool) -> bool:
    """Verifies if a plain password is equal to an hashed one"""
    return pwd_context.verify(plain_password, hashed_password)
