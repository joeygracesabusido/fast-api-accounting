from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import PlainTextResponse

from routes.admin import admin
from routes.client import client
from routes.zamboanga_client import zamboanga_client
from routes.rizal_project import rizal_project
from routes.employee_user import employee_user
from routes.tvi import tviProject
from routes.grc_employee import grcRouter
from routes.developer import developer

from mysql.connector import connect
from fastapi.staticfiles import StaticFiles

# from config.database import database

app = FastAPI()

# origins = [
#     "*",
# ]
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/favicon.ico")
async def disable_favicon():
    return PlainTextResponse("Favicon not found", status_code=404)

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
app.include_router(employee_user)
app.include_router(tviProject)
app.include_router(grcRouter)
app.include_router(developer)




# @app.on_event("startup")
# async def startup():
#     await database.connect()


# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()