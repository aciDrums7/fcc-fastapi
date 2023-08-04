""" Posts APIs """
from typing import Union

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas import posts_schemas
from app.services import posts_service
from app.exceptions.exception_handling import (
    NotFoundException,
    raise_not_found_exception,
    raise_internal_server_error,
)


router = APIRouter(prefix="/posts", tags=["Posts"])


""" GET """


@router.get("", response_model=list[posts_schemas.Post])
def get_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get Posts"""
    try:
        posts = posts_service.get_posts(db, skip, limit)

        return posts

    except Exception as err:
        raise_internal_server_error(err)


@router.get("/latest", response_model=Union[posts_schemas.Post, None])
def get_latest_post(db: Session = Depends(get_db)):
    """Get Latest Post"""
    try:
        post = posts_service.get_latest_post(db)

        return post

    except Exception as err:
        raise_internal_server_error(err)


#! If you change the order of this 2 GET requests ⬆⬇, you'll get an error!


@router.get("/{post_id}", response_model=posts_schemas.Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Get Post"""
    try:
        post = posts_service.get_post(db, post_id)
        if post == None:
            raise NotFoundException

        return post

    except NotFoundException as err:
        raise_not_found_exception(err)
    except Exception as err:
        raise_internal_server_error(err)


""" POST """


@router.post("", status_code=status.HTTP_201_CREATED, response_model=posts_schemas.Post)
def create_post(post: posts_schemas.PostUpsert, db: Session = Depends(get_db)):
    """Create a new post"""
    try:
        db_post = posts_service.create_post(db, post)

        return db_post

    except Exception as err:
        raise_internal_server_error(err)


""" PUT """


@router.put("/{post_id}")
def update_post(
    post_id: int, post: posts_schemas.PostUpsert, db: Session = Depends(get_db)
):
    """Update a Post"""
    try:
        db_post = posts_service.get_post(db, post_id)
        if db_post is None:
            raise NotFoundException
        updated_post = posts_service.update_post(db, post_id, post)

        return updated_post

    except NotFoundException as err:
        raise_not_found_exception(err)
    except Exception as err:
        raise_internal_server_error(err)


""" DELETE """


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """Delete a post"""
    try:
        deleted_post = posts_service.delete_post(db, post_id)
        if deleted_post is None:
            raise NotFoundException

        return None

    except NotFoundException as err:
        raise_not_found_exception(err)
    except Exception as err:
        raise_internal_server_error(err, post_id)
