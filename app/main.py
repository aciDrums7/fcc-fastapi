""" Basic CRUD using FastAPI """
from typing import Union

from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from app import models, crud, schemas, exception_handling
from app.exception_handling import NotFoundException
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

fastAPI = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as err:
        print(err)
    finally:
        db.close()


""" GET """


@fastAPI.get("/")
def root():
    """Hello World"""
    return {"message": "Hello World"}


@fastAPI.get("/posts", response_model=list[schemas.Post])
def get_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get Posts"""
    try:
        return crud.get_posts(db, skip=skip, limit=limit)
    except Exception as err:
        exception_handling.raise_internal_server_error(err)


@fastAPI.get("/posts/latest", response_model=Union[schemas.Post, None])
def get_latest_post(db: Session = Depends(get_db)):
    """Get Latest Post"""
    try:
        post = crud.get_latest_post(db)

        return post
    except Exception as err:
        exception_handling.raise_internal_server_error(err)


#! If you change the order of this 2 GET requests ⬆⬇, you'll get an error!


@fastAPI.get("/posts/{post_id}", response_model=schemas.Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Get Post"""
    try:
        post = crud.get_post(db, post_id)
        if post == None:
            raise NotFoundException

        return post
    except NotFoundException as err:
        exception_handling.raise_not_found_exception(err, post_id)
    except Exception as err:
        exception_handling.raise_internal_server_error(err)


""" POST """


@fastAPI.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostUpsert, db: Session = Depends(get_db)):
    """Create a new post"""
    try:
        db_post = crud.create_post(db, post)

        return db_post
    except Exception as err:
        exception_handling.raise_internal_server_error(err)


""" PUT """


@fastAPI.put("/posts/{post_id}")
def update_post(post_id: int, post: schemas.PostUpsert, db: Session = Depends(get_db)):
    """Update a Post"""
    try:
        db_post = crud.get_post(db, post_id)
        if db_post is None:
            raise NotFoundException
        updated_post = crud.update_post(db, post_id, post)

        return updated_post
    except NotFoundException as err:
        exception_handling.raise_not_found_exception(err, post_id)
    except Exception as err:
        exception_handling.raise_internal_server_error(err)


""" DELETE """


@fastAPI.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """Delete a post"""
    try:
        crud.delete_post(db, post_id)

        return None
    except Exception as err:
        exception_handling.raise_not_found_exception(err, post_id)
