""" Basic CRUD using FastAPI """
from typing import Optional, Tuple
from random import randrange
from fastapi import FastAPI, Path, Body, status, HTTPException

# from fastapi.params import Body

# ? pydantic is useful for data validation (request body/params) + schema definition
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    """Class Post"""

    id: Optional[int] = None
    title: str = None
    content: str = None
    # 1 if not provided, default value will be False
    published: bool = False
    # 2 optional value, if not provided, default value will be None
    rating: Optional[int] = None


my_posts: list[Post] = [
    Post(**{"id": 1, "title": "post 1", "content": "content of post 1"}),
    Post(**{"id": 2, "title": "post 2", "content": "content of post 2"}),
]


def find_post(id: int) -> Optional[Tuple[int, Post]]:
    return next(
        (index, Post(**post)) for index, post in enumerate(my_posts) if post["id"] == id
    )


def raise_not_found_exception(exc: Exception, id: int) -> None:
    err: str = f"Post with id: {id} not found"
    print(err)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err) from exc


@app.get("/")
def root():
    """Hello World"""
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    """Get Posts"""
    return {"data": my_posts}


@app.get("/posts/latest")
def get_latest_post():
    """Get Latest Post"""
    post = my_posts[len(my_posts) - 1]
    return {"data": post}


#! If you change the order of this 2 GET requests, you'll get an error!
@app.get("/posts/{id}")
def get_post(id: int = Path(..., title="Post ID")):
    """Get Post"""
    post: Post = None
    try:
        post = find_post(id)
    except StopIteration as exc:
        raise_not_found_exception(exc, id)

    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post = Body(..., embed=True, title="Post")):
    """Create a new post"""
    post.id = randrange(0, 10000000)
    my_posts.append(post)
    return {"data": post}


@app.put("/posts/{id}")
def update_post(
    id: int = Path(..., title="Post ID"),
    post: Post = Body(..., embed=True, title="Post"),
):
    """Update a post"""
    saved_post: Post
    try:
        saved_post_index, saved_post = find_post(id)
        saved_post = post
        saved_post.id = id
        my_posts[saved_post_index] = saved_post

    except StopIteration as exc:
        raise_not_found_exception(exc, id)

    return {"data": my_posts[saved_post_index]}


@app.patch("/posts/{id}")
def update_post_partial(id: int, post: Post):
    """Update a post property"""
    try:
        saved_post_index, saved_post = find_post(id)
        update_data = post.model_dump(exclude_unset=True)
        updated_post = saved_post.model_copy(update=update_data)
        my_posts[saved_post_index] = updated_post.model_dump()
    except StopIteration as exc:
        raise_not_found_exception(exc, id)

    return {"data": my_posts[saved_post_index]}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int = Path(..., title="Post ID")):
    """Delete a post"""
    post_index: int
    try:
        post_index = find_post(id)[0]
        my_posts.pop(post_index)
    except StopIteration as exc:
        raise_not_found_exception(exc, id)

    return None
