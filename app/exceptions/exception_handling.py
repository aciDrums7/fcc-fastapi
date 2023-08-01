""" Custom Exceptions File """
from fastapi import HTTPException, status


class NotFoundException(Exception):
    """SQL NotFoundException"""


def raise_not_found_exception(err: Exception, id: int) -> None:
    """Raise a 404: Not Found Exception"""
    err_msg: str = f"Post with id: {id} not found"
    print(err_msg)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"{err_msg}"
    ) from err


def raise_internal_server_error(err: Exception) -> None:
    """Raise a 500: Internal Server Error"""
    print(err)
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{err}"
    ) from err
