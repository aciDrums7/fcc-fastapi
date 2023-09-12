""" Posts Service """
from typing import Optional
from sqlalchemy.orm import Session
from app.repositories import posts_repository
from app.exceptions.http_exceptions import (
    ForbiddenException,
    NotFoundException,
)
from app.models.posts_model import PostModel
from app.schemas.posts_schemas import PostOut, PostUpsert
from app.schemas.users_schemas import UserOut

# * GET


def get_posts_with_n_votes(
    db_session: Session,
    skip: int,
    limit: int,
    search: Optional[str],
) -> list[PostOut]:
    """Get Posts With Number Of Votes"""
    db_posts = posts_repository.get_posts_with_n_votes(db_session, skip, limit, search)

    posts = []

    for post_model, n_votes in db_posts:
        post_schema = PostOut.model_validate(post_model)
        post_schema.n_votes = n_votes
        posts.append(post_schema)

    return posts


def get_post_by_id_with_n_votes(
    db_session: Session,
    post_id: int,
) -> PostOut:
    """Get Post By Id With Number Of Votes"""
    try:
        post_model, n_votes = posts_repository.get_post_by_id_with_n_votes(
            db_session, post_id
        )

        post_schema = PostOut.model_validate(post_model)
        post_schema.n_votes = n_votes

        return post_schema
    except TypeError as exc_404:
        raise NotFoundException(f"Post with id: {post_id} not found") from exc_404


def get_latest_post_with_n_votes(
    db_session: Session,
) -> PostOut:
    """Get Latest Post With Number Of Votes"""
    post_model, n_votes = posts_repository.get_latest_post_with_n_votes(db_session)

    if not post_model:
        raise NotFoundException("Latest post not found")

    post_schema = PostOut.model_validate(post_model)
    post_schema.n_votes = n_votes

    return post_schema


# * POST


def create_post(
    db_session: Session,
    post: PostUpsert,
    current_user: UserOut,
) -> PostOut:
    """Create Post"""
    # ? Instead of passing each of the keyword arguments to models.Post
    # 1 we are passing the dict's key-value pairs as the keyword arguments (**kwargs)
    # 3 to the SQLAlchemy Post (models.Post)
    db_post = PostModel(owner_id=current_user.id, **post.model_dump())
    db_session.add(db_post)

    db_session.commit()
    db_session.refresh(db_post)

    return PostOut.model_validate(db_post)


# * PUT


def update_post(
    db_session: Session,
    post_id: int,
    post_updated: PostUpsert,
    current_user: UserOut,
) -> PostOut:
    """Update Post"""
    db_post = posts_repository.get_post_by_id(db_session, post_id)

    if not db_post:
        raise NotFoundException(f"Post with id: {post_id} not found")
    if db_post.owner_id != current_user.id:
        raise ForbiddenException("Not authorized to perform requested action")

    for attr, value in post_updated.model_dump(exclude_unset=True).items():
        setattr(db_post, attr, value)

    db_session.commit()
    db_session.refresh(db_post)

    return PostOut.model_validate(db_post)


# * DELETE


def delete_post(db_session: Session, post_id: int, current_user: UserOut) -> None:
    """Delete a post"""
    db_post = posts_repository.get_post_by_id(db_session, post_id)

    if not db_post:
        raise NotFoundException(f"Post with id: {post_id} not found")
    if db_post.owner_id != current_user.id:
        raise ForbiddenException("Not authorized to perform requested action")

    db_session.delete(db_post)
    db_session.commit()

    return None
