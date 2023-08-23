""" fastAPI entrypoint """
from dotenv import load_dotenv
from fastapi import FastAPI
from .database.db_config import Base, Engine
from .APIs.auth_api import router as auth_router
from .APIs.users_api import router as users_router
from .APIs.posts_api import router as posts_router
from .APIs.votes_api import router as votes_router

load_dotenv(verbose=True)

Base.metadata.create_all(bind=Engine)

app = FastAPI()


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(posts_router)
app.include_router(votes_router)
