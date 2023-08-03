""" Custom Exceptions File """
from fastapi import HTTPException, status


class NotFoundException(Exception):
    """SQL NotFoundException"""


class InvalidCredentialsException(Exception):
    """Invalid Credentials Exception"""


def raise_internal_server_error(err: Exception) -> None:
    """Raise a 500: Internal Server Error"""
    print(err)
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{err}"
    ) from err


def raise_not_found_exception(err: Exception) -> None:
    """Raise a 404: Not Found Exception"""
    err_msg: str = "Record Not Found"
    print(err_msg)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err_msg) from err


def raise_invalid_credentials(err: Exception) -> None:
    """Raise a 404: Not Found Exception"""
    err_msg: str = "Invalid Credentials"
    print(err_msg)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err_msg) from err
