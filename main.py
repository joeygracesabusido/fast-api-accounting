from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.admin import admin
from routes.client import client
from routes.zamboanga_client import zamboanga_client

# from config.database import database

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
app.include_router(zamboanga_client)


# @app.on_event("startup")
# async def startup():
#     await database.connect()


# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()