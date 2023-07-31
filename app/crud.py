""" CRUD Interface """
from typing import List, Optional
from sqlalchemy import desc
from sqlalchemy.orm import Session

from . import models, schemas

""" GET """


def get_posts(db: Session, skip: int = 0, limit: int = 100) -> list[schemas.Post]:
    """Get Posts"""
    return db.query(models.Post).offset(skip).limit(limit).all()


def get_post(db: Session, post_id: int) -> Optional[schemas.Post]:
    """Get Post By Id"""
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def get_latest_post(db: Session) -> Optional[schemas.Post]:
    """Get Latest Post"""
    return db.query(models.Post).order_by(desc(models.Post.id)).first()


""" POST """


def create_post(db: Session, post: schemas.PostUpsert) -> Optional[schemas.Post]:
    """Create Post"""
    # ? Instead of passing each of the keyword arguments to models.Post
    # 1 we are passing the dict's key-value pairs as the keyword arguments (**kwargs)
    # 3 to the SQLAlchemy Post (models.Post)
    db_post = models.Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


def update_post(
    db: Session, post_id: int, post: schemas.PostUpsert
) -> Optional[schemas.Post]:
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


def delete_post(db: Session, post_id: int) -> Optional[schemas.Post]:
    """Delete a post"""
    db_post = get_post(db, post_id)
    if db_post is None:
        return None
    db.delete(db_post)
    db.commit()

    return db_post
