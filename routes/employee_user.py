import json
from lib2to3.pgen2 import token
from pyexpat import model
from re import I
from urllib import response
from urllib.request import Request
from fastapi import APIRouter, Body, HTTPException, Depends,status,Response
from typing import Union, List
from datetime import datetime

from bson import ObjectId
from typing import Optional


from models.model import EmployeeUser


from config.db import mydb


from jose import jwt

JWT_SECRET = 'myjwtsecret'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

employee_user = APIRouter(include_in_schema=False)



from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)


def validateLogin(request:Request):
    """This function is for Log In Authentication"""
    
    try :
        token = request.cookies.get('access_token')
        # print(token)
        if token is None:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Not Authorized",
            # headers={"WWW-Authenticate": "Basic"},
            )
        else:
            scheme, _, param = token.partition(" ")
            payload = jwt.decode(param, JWT_SECRET, algorithms=ALGORITHM)
        
            username = payload.get("sub")
        

            user =  mydb.employee_login.find({"username":username})

            if user is not None:

                return username

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Not Authorized Please login",
            # headers={"WWW-Authenticate": "Basic"},
        )


@employee_user.post('/api-employee-sign-up/')
def employee_sign_up(items:EmployeeUser):
    """This function is for inserting """
    dataInsert = dict()
    try:
        dataInsert = {
            "fullname": items.fullname,
            "username": items.username,
            "password": get_password_hash(items.password),
            "status": items.status,
            "created": items.created
            
            }
        mydb.employee_login.insert_one(dataInsert)
    
    except Exception as ex:
        print("Error", f"Error due to :{str(ex)}")
    return {"message":"User has been save"} 

