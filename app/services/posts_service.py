""" Posts Service """
from typing import List, Optional
from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.models import posts_model
from app.schemas import posts_schemas

""" GET """


def get_posts(db: Session, skip: int = 0, limit: int = 100) -> list[posts_schemas.Post]:
    """Get Posts"""
    return (
        db.query(posts_model.Post)
        .order_by(posts_model.Post.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_post(db: Session, post_id: int) -> Optional[posts_schemas.Post]:
    """Get Post By Id"""
    return db.query(posts_model.Post).filter(posts_model.Post.id == post_id).first()


def get_latest_post(db: Session) -> Optional[posts_schemas.Post]:
    """Get Latest Post"""
    return db.query(posts_model.Post).order_by(desc(posts_model.Post.id)).first()


""" UPSERT """


def create_post(
    db: Session, post: posts_schemas.PostUpsert
) -> Optional[posts_schemas.Post]:
    """Create Post"""
    # ? Instead of passing each of the keyword arguments to models.Post
    # 1 we are passing the dict's key-value pairs as the keyword arguments (**kwargs)
    # 3 to the SQLAlchemy Post (models.Post)
    db_post = posts_model.Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


def update_post(
    db: Session, post_id: int, post: posts_schemas.PostUpsert
) -> Optional[posts_schemas.Post]:
    """Update Post"""
    db_post = get_post(db, post_id)
    if db_post is None:
        return None
    # ? The commented code doesn't work because we create a new instance of a Post object
    # ? We need to modify the already existing instance, as did with the for loop below
    # * db_post = models.Post(**post.model_dump(exclude_unset=True))
    for attr, value in post.model_dump(exclude_unset=True).items():
        setattr(db_post, attr, value)
    db.commit()
    db.refresh(db_post)

    return db_post


""" DELETE """


def delete_post(db: Session, post_id: int) -> Optional[posts_schemas.Post]:
    """Delete a post"""
    db_post = get_post(db, post_id)
    if db_post is None:
        return None
    db.delete(db_post)
    db.commit()

    return db_post