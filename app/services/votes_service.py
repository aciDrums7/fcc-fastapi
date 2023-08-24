""" Votes Service """
from sqlalchemy.orm import Session
from app.repositories import votes_repository
from app.exceptions.http_exceptions import (
    ConflictException,
    NotFoundException,
)
from app.models.votes_model import VoteModel
from app.schemas.votes_schemas import VotePayload, VoteOut
from app.schemas.users_schemas import UserOut
from app.services import posts_service


def create_or_delete_vote(
    db_session: Session,
    vote: VotePayload,
    current_user: UserOut,
) -> VoteOut | None:
    """Create Vote"""
    # ? Check if post associated to vote does exist
    posts_service.get_post_by_id_with_n_votes(db_session, vote.post_id, current_user)

    db_vote = votes_repository.get_vote(db_session, vote, current_user)

    if vote.dir == 1:
        if db_vote:
            raise ConflictException(
                f"User with id: {current_user.id} has already voted on post with id: {vote.post_id}"
            )
        else:
            db_vote = VoteModel(user_id=current_user.id, post_id=vote.post_id)
            db_session.add(db_vote)
            db_session.commit()
            db_session.refresh(db_vote)

            return VoteOut.model_validate(db_vote)
    # ? vote.dir == 0 means we want to delete a vote
    else:
        if not db_vote:
            raise NotFoundException(
                f"Vote with user_id: {current_user.id} and post_id: {vote.post_id} not found"
            )
        else:
            # vote_query.delete(synchronize_session=False)
            db_session.delete(db_vote)
            db_session.commit()
            return None
