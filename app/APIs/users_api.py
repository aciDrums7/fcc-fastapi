""" Users APIs """

from fastapi import APIRouter, Depends, status
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import users_schemas
from ..services import users_service
from ..exceptions import exception_handling
from ..exceptions.exception_handling import NotFoundException

router = APIRouter()

# TODO: implement all the APIs

""" GET """


""" UPSERT """


""" DELETE """
