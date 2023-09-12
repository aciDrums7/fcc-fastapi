""" Posts APIs """
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.db_config import get_db
from app.schemas.users_schemas import UserOut
from app.schemas.posts_schemas import PostOut, PostUpsert
from app.services import posts_service
from app.exceptions.http_exceptions import (
    UnauthorizedException,
    ForbiddenException,
    NotFoundException,
    InternalServerErrorException,
)
from app.authentication import oauth2_service

router = APIRouter(prefix="/posts", tags=["Posts"])


# 5 GET


@router.get("", response_model=list[PostOut])
def get_posts(
    skip: int = 0,
    limit: int = 100,
    search: str = "",
    db_session: Session = Depends(get_db),
    current_user: UserOut = Depends(oauth2_service.get_current_user),
):
    """Get Posts"""
    try:
        posts = posts_service.get_posts_with_n_votes(db_session, skip, limit, search)

        return posts

    except Exception as exc_500:
        print(exc_500)
        raise InternalServerErrorException(exc_500) from exc_500


@router.get("/latest", response_model=PostOut)
def get_latest_post(
    db_session: Session = Depends(get_db),
    current_user: UserOut = Depends(oauth2_service.get_current_user),
):
    """Get Latest Post"""
    try:
        post = posts_service.get_latest_post_with_n_votes(db_session)
        return post

    except NotFoundException as exc_404:
        print(exc_404)
        raise exc_404
    except Exception as exc_500:
        print(exc_500)
        raise InternalServerErrorException(exc_500) from exc_500


#! If you change the order of this 2 GET requests ⬆⬇, you'll get an error!


@router.get("/{post_id}", response_model=PostOut)
def get_post(
    post_id: int,
    db_session: Session = Depends(get_db),
    current_user: UserOut = Depends(oauth2_service.get_current_user),
):
    """Get Post"""
    try:
        post = posts_service.get_post_by_id_with_n_votes(db_session, post_id)
        return post

    except ForbiddenException as exc_403:
        print(exc_403)
        raise exc_403
    except NotFoundException as exc_404:
        print(exc_404)
        raise exc_404
    except Exception as exc_500:
        print(exc_500)
        raise InternalServerErrorException(exc_500) from exc_500


# 5 POST


@router.post("", status_code=status.HTTP_201_CREATED, response_model=PostOut)
def create_post(
    post: PostUpsert,
    db_session: Session = Depends(get_db),
    current_user: UserOut = Depends(oauth2_service.get_current_user),
):
    """Create a new post"""
    try:
        db_post = posts_service.create_post(db_session, post, current_user)
        return db_post

    except Exception as exc_500:
        print(exc_500)
        raise InternalServerErrorException(exc_500) from exc_500


# 5 PUT


@router.put("/{post_id}", response_model=PostOut)
def update_post(
    post_id: int,
    post: PostUpsert,
    db_session: Session = Depends(get_db),
    current_user: UserOut = Depends(oauth2_service.get_current_user),
):
    """Update a Post"""
    try:
        updated_post = posts_service.update_post(
            db_session, post_id, post, current_user
        )
        return updated_post

    except UnauthorizedException as exc_401:
        print(exc_401)
        raise exc_401
    except ForbiddenException as exc_403:
        print(exc_403)
        raise exc_403
    except NotFoundException as exc_404:
        print(exc_404)
        raise exc_404
    except Exception as exc_500:
        print(exc_500)
        raise InternalServerErrorException(exc_500) from exc_500


# 5 DELETE


@router.delete(
    "/{post_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
def delete_post(
    post_id: int,
    db_session: Session = Depends(get_db),
    current_user: UserOut = Depends(oauth2_service.get_current_user),
):
    """Delete a post"""
    try:
        posts_service.delete_post(db_session, post_id, current_user)
        return None

    except UnauthorizedException as exc_401:
        print(exc_401)
        raise exc_401
    except ForbiddenException as exc_403:
        print(exc_403)
        raise exc_403
    except NotFoundException as exc_404:
        print(exc_404)
        raise exc_404
    except Exception as exc_500:
        print(exc_500)
        raise InternalServerErrorException(exc_500) from exc_500
