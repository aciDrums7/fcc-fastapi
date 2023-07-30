""" Basic CRUD using FastAPI """
import time
from typing import Optional, Tuple

# from random import randrange
from fastapi import FastAPI, Path, Body, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor

# ? pydantic is useful for data validation (request body/params) + schema definition
from pydantic import BaseModel

app = FastAPI()

""" CLASSES """


class Post(BaseModel):
    """Class Post"""

    id: Optional[int] = None
    title: str = None
    content: str = None
    # 1 if not provided, default value will be False
    published: bool = False
    # 2 optional value, if not provided, default value will be None
    rating: Optional[int] = None


class NotFoundException(Exception):
    """SQL NotFoundException"""


""" DB CONNECTION """

while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastAPI",
            user="postgres",
            password="postgres",
            cursor_factory=RealDictCursor,
        )
        db = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as err:
        print("Connecting to database failed")
        print("Error: ", err)
        time.sleep(3)

""" UTILS """

my_posts: list[Post] = [
    Post(**{"id": 1, "title": "post 1", "content": "content of post 1"}),
    Post(**{"id": 2, "title": "post 2", "content": "content of post 2"}),
]


def find_post(id: int) -> Optional[Tuple[int, Post]]:
    """Find Post by id"""
    return next(
        (index, Post(**post)) for index, post in enumerate(my_posts) if post.id == id
    )


""" ERRORS """


def raise_not_found_exception(err: Exception, id: int) -> None:
    """Raise a 404: Not Found Exception"""
    err_msg: str = f"Post with id: {id} not found"
    print(err_msg)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"{err_msg}"
    ) from err


def raise_internal_server_error(err: Exception) -> None:
    """Raise a 500: Internal Server Error"""
    print(err)
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{err}"
    ) from err


""" GET """


@app.get("/")
def root():
    """Hello World"""
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    """Get Posts"""
    try:
        db.execute("SELECT * FROM posts ORDER BY id ASC")
        posts = db.fetchall()

        return {"data": posts}
    except Exception as err:
        raise_internal_server_error(err)


@app.get("/posts/latest")
def get_latest_post():
    """Get Latest Post"""
    try:
        db.execute("SELECT * FROM posts ORDER BY id DESC LIMIT 1")
        post = db.fetchone()

        return {"data": post}
    except Exception as err:
        raise_internal_server_error(err)


#! If you change the order of this 2 GET requests ⬆⬇, you'll get an error!


@app.get("/posts/{id}")
def get_post(id: int):
    """Get Post"""
    try:
        db.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
        post = db.fetchone()
        if post == None:
            raise NotFoundException

        return {"data": post}
    except NotFoundException as err:
        raise_not_found_exception(err, id)
    except Exception as err:
        raise_internal_server_error(err)


""" POST """


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(request_post: Post):
    """Create a new post"""
    try:
        db.execute(
            "INSERT INTO posts (title, content, published, rating) VALUES (%s, %s, %s, %s) RETURNING *",
            (
                request_post.title,
                request_post.content,
                request_post.published,
                request_post.rating,
            ),
        )
        saved_post = db.fetchone()
        conn.commit()

        return {"data": saved_post}
    except Exception as err:
        raise_internal_server_error(err)


""" PUT """


@app.put("/posts/{id}")
def update_post(
    id: int,
    request_post: Post,
):
    """Update a post"""
    try:
        db.execute(
            "UPDATE posts SET title = %s, content = %s, published = %s, rating = %s WHERE id = %s RETURNING *",
            (
                request_post.title,
                request_post.content,
                request_post.published,
                request_post.rating,
                id,
            ),
        )
        updated_post = db.fetchone()
        if updated_post == None:
            raise NotFoundException
        conn.commit()

        return {"data": updated_post}
    except NotFoundException as err:
        raise_not_found_exception(err, id)
    except Exception as err:
        raise_internal_server_error(err)


""" PATCH """


@app.patch("/posts/{id}")
def update_post_partial(id: int, request_post: Post):
    """Update a post property"""
    try:
        saved_post_index, saved_post = find_post(id)
        update_data = request_post.model_dump(exclude_unset=True)
        updated_post = saved_post.model_copy(update=update_data)
        my_posts[saved_post_index] = updated_post.model_dump()
    except StopIteration as err:
        raise_not_found_exception(err, id)

    return {"data": my_posts[saved_post_index]}


""" DELETE """


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    """Delete a post"""
    try:
        db.execute("DELETE FROM posts WHERE id = %s RETURNING * ", (str(id),))
        deleted_post = db.fetchone()
        if deleted_post == None:
            raise Exception
        conn.commit()
        return None
    except Exception as err:
        print(err)
        raise_not_found_exception(err, id)
