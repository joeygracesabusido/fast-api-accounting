from traceback import format_list
from fastapi import APIRouter, Body, HTTPException, Depends, Request, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from config.db import mydb


from bson import ObjectId
from typing import Optional

from datetime import timedelta, datetime


from jose import jwt

JWT_SECRET = 'myjwtsecret'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

tviProject = APIRouter(include_in_schema=False)


templates = Jinja2Templates(directory="templates")


#==================================================This is for user validation====================================
from schemas.user import usersEntity
def validateLogin(request:Request):

    try :
        token = request.cookies.get('access_token')
        if token is None:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Not Authorized",
           
            )
        else:
            scheme, _, param = token.partition(" ")
            payload = jwt.decode(param, JWT_SECRET, algorithms=ALGORITHM)
        
            username = payload.get("sub")
            user =  usersEntity(mydb.login.find({"username":username}))
            

            if user == [] :
                 raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= "Not Authorized",
                
                )
            else:
                
                return username

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Not Authorized please Login",
            # headers={"WWW-Authenticate": "Basic"},
        )

from config.tviDB import TviDB
TviDB.initialize() # this is to inialized database of TVI



@tviProject.get("/tvi-transaction/", response_class=HTMLResponse)
async def getTviTrans(request:Request,username: str = Depends(validateLogin)):
    """This function is for querying income statement"""
    return templates.TemplateResponse("tvi/tviEquipment.html",{'request':request})

