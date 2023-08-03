""" fastAPI entrypoint """

from fastapi import FastAPI

from .database import Base, Engine
from .APIs.posts_api import router as posts_router
from .APIs.users_api import router as users_router
from .APIs.auth_api import router as auth_router

Base.metadata.create_all(bind=Engine)

app = FastAPI()


app.include_router(users_router)
app.include_router(posts_router)
app.include_router(auth_router)
