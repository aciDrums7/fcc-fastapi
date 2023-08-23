""" Custom Exceptions File """
from fastapi import HTTPException, status


# 400
class UnauthorizedException(HTTPException):
    """401 Unauthorized Exception"""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{detail}",
            headers={"WWW-Authenticate": "Bearer"},
        )


class ForbiddenException(HTTPException):
    """403 Forbidden Exception"""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{detail}",
        )


class NotFoundException(HTTPException):
    """404: Not Found Exception"""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{detail}",
        )


class ConflictException(HTTPException):
    """409: Conflict Exception"""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{detail}",
        )


# 500
class InternalServerErrorException(HTTPException):
    """500: Internal Server Error Exception"""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{detail}",
        )
