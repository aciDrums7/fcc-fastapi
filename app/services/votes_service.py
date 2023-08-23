""" Votes Service """
from typing import Union
from sqlalchemy.orm import Session
from app.exceptions.http_exceptions import (
    ConflictException,
    NotFoundException,
)
from app.models import votes_model
from app.schemas import votes_schemas, users_schemas
from app.services import posts_service


def create_or_delete_vote(
    db_session: Session,
    vote: votes_schemas.Vote,
    current_user: users_schemas.User,
) -> Union[votes_schemas.Vote, None]:
    """Create Vote"""
    # ? Check if post associated to vote does exist
    posts_service.get_post_by_id(db_session, vote.post_id, current_user)

    vote_query = db_session.query(votes_model.Vote).filter(
        votes_model.Vote.post_id == vote.post_id,
        votes_model.Vote.user_id == current_user.id,
    )
    db_vote = vote_query.first()
    if vote.dir == 1:
        if db_vote:
            raise ConflictException(
                f"User with id: {current_user.id} has already voted on post with id: {vote.post_id}"
            )
        else:
            db_vote = votes_model.Vote(user_id=current_user.id, post_id=vote.post_id)
            db_session.add(db_vote)
            db_session.commit()
            db_session.refresh(db_vote)

            return db_vote
    # ? vote.dir == 0 means we want to delete a vote
    else:
        if not db_vote:
            raise NotFoundException(
                f"Vote with user_id: {current_user.id} and post_id: {vote.post_id} not found"
            )
        else:
            vote_query.delete(synchronize_session=False)
            db_session.commit()
            return None
