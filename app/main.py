""" fastAPI entrypoint """
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database.db_config import Base, Engine
from .APIs.auth_api import router as auth_router
from .APIs.users_api import router as users_router
from .APIs.posts_api import router as posts_router
from .APIs.votes_api import router as votes_router

load_dotenv(verbose=True)

# ? Don't need this once Alembic is implemented
# Base.metadata.create_all(bind=Engine)

app = FastAPI()

origins = [
    "https://www.google.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(posts_router)
app.include_router(votes_router)


@app.get("/", response_model=str)
def hello_world():
    return "Hello World!"
