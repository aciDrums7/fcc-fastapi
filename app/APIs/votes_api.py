""" Votes APIs """
from fastapi import APIRouter, Depends, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.database.db_config import get_db
from app.schemas.users_schemas import UserOut
from app.schemas.votes_schemas import VotePayload
from app.services import votes_service
from app.exceptions.http_exceptions import (
    ConflictException,
    NotFoundException,
    InternalServerErrorException,
)
from app.authentication import oauth2_service

router = APIRouter(prefix="/votes", tags=["Votes"])

# * POST


@router.post("", status_code=status.HTTP_201_CREATED, response_model=None)
async def create_or_delete_vote(
    vote: VotePayload,
    db_session: Session = Depends(get_db),
    current_user: UserOut = Depends(oauth2_service.get_current_user),
):
    """Create Vote"""
    try:
        db_vote = votes_service.create_or_delete_vote(db_session, vote, current_user)
        if not db_vote:
            return Response(
                content=None,
                status_code=status.HTTP_204_NO_CONTENT,
                headers={"Content-Length": "0"},
            )
        return db_vote

    except NotFoundException as exc_404:
        print(exc_404)
        raise exc_404
    except ConflictException as exc_409:
        print(exc_409)
        raise exc_409
    except Exception as exc_500:
        print(exc_500)
        raise InternalServerErrorException(exc_500) from exc_500
