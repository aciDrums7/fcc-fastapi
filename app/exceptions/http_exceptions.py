""" Custom Exceptions File """
from fastapi import HTTPException, status


class InternalServerErrorException(HTTPException):
    """500: Internal Server Error Exception"""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{detail}",
        )


class NotFoundException(HTTPException):
    """404: Not Found Exception"""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{detail}",
        )


class UnauthorizedException(HTTPException):
    """401 Unauthorized Exception"""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{detail}",
            headers={"WWW-Authenticate": "Bearer"},
        )