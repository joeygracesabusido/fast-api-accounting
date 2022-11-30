import json
from lib2to3.pgen2 import token
from pyexpat import model
from re import I

from fastapi import APIRouter, Body, HTTPException, Depends, Request, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Union, List
from datetime import datetime

from bson import ObjectId
from typing import Optional


from datetime import timedelta, datetime,date


from models.model import EmployeeUser


from config.db import mydb


from jose import jwt

JWT_SECRET = 'myjwtsecret'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

employee_user = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")



from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

password1 = ""
def authenticate_user(username, password):
    
    user = mydb.employee_login.find({'$and':[{"username":username},{'status':'Approved'}]})

    for i in user:
        username = i['username']
        password1 = i['password']
        
   
        if user:
            
            password_check = pwd_context.verify(password,password1)
            
            return password_check

            
        else :
            False



def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()

    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})

    
    return to_encode

  



@employee_user.post('/employee-login/')
async def login(response: Response, request:Request):
    form =  await request.form()
    username = form.get('username')
    password = form.get('password')

    
    
    errors =[]
    msg = []
    try:
        if authenticate_user(username, password):
            access_token = create_access_token(
                data = {"sub": username}, 
                expires_delta=timedelta(minutes=30)
                                    )
          
            
            
            token = jwt.encode(access_token, JWT_SECRET,algorithm=ALGORITHM)
            
            msg.append('Login Succesful')
            response = templates.TemplateResponse("login.html", {"request":request,"msg":msg})
            response.set_cookie(key="access_token", value=f'Bearer {token}',httponly=True)
            return response
            
           

        else :
            msg.append('Incorrect username or password')
            # raise HTTPException(status_code=400, detail="Incorrect username or password")
            return templates.TemplateResponse("login.html", {"request":request,"msg":msg})
    except:
        errors.append('Something wrong')
        return templates.TemplateResponse("login.html", {"request":request,"msg":msg})

#======================================Login for Front End or API Login=============================
@employee_user.get("/employee-login/", response_class=HTMLResponse)
async def api_login(request: Request):
    return templates.TemplateResponse("login_api.html", {"request":request}) 

def EmployeevalidateLogin(request:Request):
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


#======================================Login for Front End or API Login=============================



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

