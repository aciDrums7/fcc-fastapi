""" Posts Service """
from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.exceptions.http_exceptions import (
    InternalServerErrorException,
    ForbiddenException,
    NotFoundException,
)
from app.models import posts_model
from app.schemas import posts_schemas, users_schemas

# * GET


def get_posts(
    db_session: Session, skip: int = 0, limit: int = 100
) -> list[posts_schemas.Post]:
    """Get Posts"""
    try:
        return (
            db_session.query(posts_model.Post)
            .order_by(posts_model.Post.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    except Exception as err:
        raise InternalServerErrorException(err) from err


def get_post_by_id(db_session: Session, post_id: int) -> posts_schemas.Post:
    """Get Post By Id"""
    try:
        db_post = (
            db_session.query(posts_model.Post)
            .filter(posts_model.Post.id == post_id)
            .first()
        )
        if not db_post:
            raise NotFoundException(f"Post with id: {post_id} not found")
        return db_post

    except Exception as err:
        raise InternalServerErrorException(err) from err


def get_latest_post(db_session: Session) -> posts_schemas.Post:
    """Get Latest Post"""
    try:
        db_post = (
            db_session.query(posts_model.Post)
            .order_by(desc(posts_model.Post.id))
            .first()
        )

        if not db_post:
            raise NotFoundException("No posts found")
        return db_post

    except Exception as err:
        raise InternalServerErrorException(err) from err


# * POST


def create_post(
    db_session: Session,
    post: posts_schemas.PostUpsert,
    current_user: users_schemas.User,
) -> posts_schemas.Post:
    """Create Post"""
    try:
        # ? Instead of passing each of the keyword arguments to models.Post
        # 1 we are passing the dict's key-value pairs as the keyword arguments (**kwargs)
        # 3 to the SQLAlchemy Post (models.Post)
        db_post = posts_model.Post(owner_id=current_user.id, **post.model_dump())
        db_session.add(db_post)

        db_session.commit()
        db_session.refresh(db_post)

        return db_post

    except Exception as err:
        raise InternalServerErrorException(err) from err


# * PUT


def update_post(
    db_session: Session,
    post_id: int,
    post: posts_schemas.PostUpsert,
    current_user: users_schemas.User,
) -> posts_schemas.Post:
    """Update Post"""
    try:
        db_post = get_post_by_id(db_session, post_id)

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
    
    except Exception as err:
        raise InternalServerErrorException(err) from err


# * DELETE


def delete_post(
    db_session: Session, post_id: int, current_user: users_schemas.User
) -> None:
    """Delete a post"""
    try:
        db_post = get_post_by_id(db_session, post_id)

        if not db_post:
            raise NotFoundException(f"Post with id: {post_id} not found")
        if db_post.owner_id != current_user.id:
            raise ForbiddenException("Not authorized to perform requested action")

        db_session.delete(db_post)
        db_session.commit()

        return None

    except Exception as err:
        raise InternalServerErrorException(err) from err
