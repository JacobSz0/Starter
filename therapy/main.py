from fastapi import FastAPI
from routers import accounts
from routers.authenticator import authenticator
from fastapi.middleware.cors import CORSMiddleware
import os


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
    os.environ.get("CORS_HOST", "REACT_APP_THERAPYHUB_API_HOST"),
    'http://localhost:8090'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(accounts.router)
app.include_router(authenticator.router)
