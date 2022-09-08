from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.admin import admin
from routes.client import client

app = FastAPI()

origins = ['https://localhost:8000']

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

app.include_router(admin)
app.include_router(client)