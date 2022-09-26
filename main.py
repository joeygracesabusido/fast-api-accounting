from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.admin import admin
from routes.client import client
from routes.zamboanga_client import zamboanga_client
from routes.rizal_project import rizal_project

# from config.database import database

app = FastAPI()

# origins = [
#     "*",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

app.include_router(admin)
app.include_router(client)
app.include_router(zamboanga_client)
app.include_router(rizal_project)


# @app.on_event("startup")
# async def startup():
#     await database.connect()


# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()