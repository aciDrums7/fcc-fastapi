""" Posts Service """
from typing import Optional
from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from app.exceptions.http_exceptions import (
    ForbiddenException,
    NotFoundException,
)
from app.models import posts_model, votes_model
from app.schemas import posts_schemas, users_schemas

# * GET


def get_posts(
    db_session: Session,
    skip: int,
    limit: int,
    search: Optional[str],
    current_user: users_schemas.User,
) -> list[posts_schemas.Post]:
    """Get Posts"""
    db_posts = (
        db_session.query(
            posts_model.Post, func.count(votes_model.Vote.post_id).label("votes")
        )
        .filter(
            posts_model.Post.owner_id == current_user.id,
            posts_model.Post.title.contains(search),
        )
        .join(
            votes_model.Vote,
            posts_model.Post.id == votes_model.Vote.post_id,
            isouter=True,
        )
        .group_by(posts_model.Post.id)
        .order_by(posts_model.Post.id)
        .limit(limit)
        .offset(skip)
    ).all()

    posts = []

    # TODO: why does this work?
    for post, n_votes in db_posts:
        post.n_votes = n_votes  # Assign n_votes to the n_votes property
        posts.append(post)

    return posts


def get_post_by_id(
    db_session: Session,
    post_id: int,
    current_user: users_schemas.User,
) -> posts_schemas.Post:
    """Get Post By Id"""
    db_post = (
        db_session.query(posts_model.Post)
        .filter(posts_model.Post.id == post_id)
        .first()
    )
    if not db_post:
        raise NotFoundException(f"Post with id: {post_id} not found")
    if db_post.owner_id is not current_user.id:
        raise ForbiddenException("Not authorized to perform requested action")
    return db_post


def get_latest_post(
    db_session: Session,
    current_user: users_schemas.User,
) -> posts_schemas.Post:
    """Get Latest Post"""
    db_post = (
        db_session.query(posts_model.Post)
        .filter(posts_model.Post.owner_id == current_user.id)
        .order_by(desc(posts_model.Post.id))
        .first()
    )

    if not db_post:
        raise NotFoundException("No posts found")
    return db_post


# * POST


def create_post(
    db_session: Session,
    post: posts_schemas.PostUpsert,
    current_user: users_schemas.User,
) -> posts_schemas.Post:
    """Create Post"""
    # ? Instead of passing each of the keyword arguments to models.Post
    # 1 we are passing the dict's key-value pairs as the keyword arguments (**kwargs)
    # 3 to the SQLAlchemy Post (models.Post)
    db_post = posts_model.Post(owner_id=current_user.id, **post.model_dump())
    db_session.add(db_post)

    db_session.commit()
    db_session.refresh(db_post)

    return db_post


# * PUT


def update_post(
    db_session: Session,
    post_id: int,
    post: posts_schemas.PostUpsert,
    current_user: users_schemas.User,
) -> posts_schemas.Post:
    """Update Post"""
    db_post = get_post_by_id(db_session, post_id, current_user)

    if not db_post:
        raise NotFoundException(f"Post with id: {post_id} not found")
    if db_post.owner_id != current_user.id:
        raise ForbiddenException("Not authorized to perform requested action")

    # ? The commented code doesn't work because we create a new instance of a Post object
    # ? We need to modify the already existing instance, as did with the for loop below
    # db_post = models.Post(**post.model_dump(exclude_unset=True))

    for attr, value in post.model_dump(exclude_unset=True).items():
        setattr(db_post, attr, value)

    db_session.commit()
    db_session.refresh(db_post)

    return db_post


# * DELETE


def delete_post(
    db_session: Session, post_id: int, current_user: users_schemas.User
) -> None:
    """Delete a post"""
    db_post = get_post_by_id(db_session, post_id, current_user)

    if not db_post:
        raise NotFoundException(f"Post with id: {post_id} not found")
    if db_post.owner_id != current_user.id:
        raise ForbiddenException("Not authorized to perform requested action")

    db_session.delete(db_post)
    db_session.commit()

    return None
