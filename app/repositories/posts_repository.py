""" Posts Repository """
from typing import Optional, List, Tuple
from sqlalchemy import func, desc
from sqlalchemy.orm import Session
from app.models.posts_model import PostModel
from app.models.votes_model import VoteModel
from app.schemas.users_schemas import UserOut

# * GET


def get_posts(
    db_session: Session,
    skip: int,
    limit: int,
    search: Optional[str],
    current_user: UserOut,
) -> List[PostModel]:
    """Get Posts"""
    db_posts = (
        db_session.query(PostModel)
        .filter(
            PostModel.owner_id == current_user.id,
            PostModel.title.contains(search),
        )
        .order_by(PostModel.id)
        .limit(limit)
        .offset(skip)
    ).all()

    return db_posts


def get_posts_with_n_votes(
    db_session: Session,
    skip: int,
    limit: int,
    search: Optional[str],
) -> List[Tuple[PostModel, int]]:
    """Get Posts With Number Of Votes"""
    db_posts = (
        db_session.query(PostModel, func.count(VoteModel.post_id).label("n_votes"))
        .filter(
            PostModel.title.contains(search),
        )
        .join(
            VoteModel,
            PostModel.id == VoteModel.post_id,
            isouter=True,
        )
        .group_by(PostModel.id)
        .order_by(PostModel.id)
        .limit(limit)
        .offset(skip)
    ).all()

    return db_posts


def get_post_by_id(
    db_session: Session,
    post_id: int,
) -> PostModel | None:
    """Get Post By Id"""
    db_post = db_session.query(PostModel).filter(PostModel.id == post_id).first()

    return db_post


def get_post_by_id_with_n_votes(
    db_session: Session,
    post_id: int,
) -> Tuple[PostModel, int] | None:
    """Get Post By Id With Number Of Votes"""
    db_post = (
        db_session.query(PostModel, func.count(VoteModel.post_id).label("n_votes"))
        .filter(PostModel.id == post_id)
        .join(
            VoteModel,
            PostModel.id == VoteModel.post_id,
            isouter=True,
        )
        .group_by(PostModel.id)
        .first()
    )

    return db_post


def get_latest_post(
    db_session: Session,
) -> PostModel | None:
    """Get Latest Post"""
    db_post = db_session.query(PostModel).order_by(desc(PostModel.id)).first()

    return db_post


def get_latest_post_with_n_votes(
    db_session: Session,
) -> Tuple[PostModel, int] | None:
    """Get Latest Post"""
    db_post = (
        db_session.query(PostModel, func.count(VoteModel.post_id).label("n_votes"))
        .join(
            VoteModel,
            PostModel.id == VoteModel.post_id,
            isouter=True,
        )
        .group_by(PostModel.id)
        .order_by(desc(PostModel.id))
        .first()
    )

    return db_post
