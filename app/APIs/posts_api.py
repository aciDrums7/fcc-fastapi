""" Posts APIs """
from typing import Union

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.posts_schemas import Post, PostUpsert
from app.schemas.token_schemas import TokenData
from app.services import posts_service
from app.exceptions.http_exceptions import (
    NotFoundException,
    InternalServerErrorException,
)
from app.authentication import oauth2


router = APIRouter(prefix="/posts", tags=["Posts"])


""" GET """


@router.get("", response_model=list[Post])
def get_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get Posts"""
    try:
        posts = posts_service.get_posts(db, skip, limit)

        return posts

    except Exception as err:
        raise InternalServerErrorException(err)


@router.get("/latest", response_model=Union[Post, None])
def get_latest_post(db: Session = Depends(get_db)):
    """Get Latest Post"""
    try:
        post = posts_service.get_latest_post(db)

        return post

    except Exception as err:
        raise InternalServerErrorException(err)


#! If you change the order of this 2 GET requests ⬆⬇, you'll get an error!


@router.get("/{post_id}", response_model=Union[Post, None])
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Get Post"""
    try:
        post = posts_service.get_post(db, post_id)
        if not post:
            raise NotFoundException(f"Post with id: {post_id} not found")

        return post

    except NotFoundException as err:
        print(err)
        raise err
    except Exception as err:
        raise InternalServerErrorException(err)


""" POST """


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Union[Post, None])
def create_post(
    post: PostUpsert,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(oauth2.get_current_user),
):
    """Create a new post"""
    try:
        db_post = posts_service.create_post(db, post)

        return db_post

    except Exception as err:
        raise InternalServerErrorException(err)


""" PUT """


@router.put("/{post_id}", response_model=Union[Post, None])
def update_post(
    post_id: int,
    post: PostUpsert,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(oauth2.get_current_user),
):
    """Update a Post"""
    try:
        db_post = posts_service.get_post(db, post_id)
        if not db_post:
            raise NotFoundException(f"Post with id: {post_id} not found")

        updated_post = posts_service.update_post(db, post_id, post)
        return updated_post

    except NotFoundException as err:
        print(err)
        raise err
    except Exception as err:
        raise InternalServerErrorException(err)


""" DELETE """


@router.delete(
    "/{post_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(oauth2.get_current_user),
):
    """Delete a post"""
    try:
        deleted_post = posts_service.delete_post(db, post_id)
        if not deleted_post:
            raise NotFoundException(f"Post with id: {post_id} not found")

        return None

    except NotFoundException as err:
        print(err)
        raise err
    except Exception as err:
        raise InternalServerErrorException(err)
