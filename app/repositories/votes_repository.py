""" Votes Repository """
from sqlalchemy.orm import Session
from app.models.votes_model import VoteModel
from app.schemas.votes_schemas import VotePayload


def get_vote(
    db_session: Session,
    vote: VotePayload,
) -> VoteModel | None:
    """Get Vote"""
    db_vote = (
        db_session.query(VoteModel)
        .filter(
            VoteModel.post_id == vote.post_id,
        )
        .first()
    )

    return db_vote
