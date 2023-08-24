""" Votes Repository """
from sqlalchemy.orm import Session
from app.models.votes_model import VoteModel
from app.schemas.votes_schemas import VotePayload
from app.schemas.users_schemas import UserOut


def get_vote(
    db_session: Session,
    vote: VotePayload,
    current_user: UserOut,
) -> VoteModel | None:
    """Get Vote"""
    db_vote = (
        db_session.query(VoteModel)
        .filter(
            VoteModel.post_id == vote.post_id,
            VoteModel.user_id == current_user.id,
        )
        .first()
    )

    return db_vote
