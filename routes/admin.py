import json
from fastapi import APIRouter, Body, HTTPException, Depends
from typing import Union
from datetime import datetime



from schemas.user import userEntity,usersEntity
from schemas.chartofAccount import chartofAccount,chartofAccounts
from models.model import User



from config.db import mydb

admin = APIRouter()

# @admin.get('/')
# def home():
#     """This is for testing only"""
#     return {"Main":"This is Lenged"}
#==================================================User Data =============================================
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

@admin.post('/sign-up')
def sign_up(fullname: str, username: str, password: str, status: str,created: Union[datetime, None] = Body(default=None)):
    """This function is for inserting """
    dataInsert = dict()
    dataInsert = {
        "fullname": fullname,
        "username": username,
        "password": get_password_hash(password),
        "status": status,
        "created": created
        
        }
    mydb.login.insert_one(dataInsert)
    return {"message":"User has been save"}

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(username, password):
    user = mydb.login.find({"username":username})

    for i in user:
        username = i['username']
        password1 = i['password']
   
        if user:
            password_check = pwd_context.verify(password,password1)
            return password_check
        else :
            False

    # user = json.loads(mydb.login.find({"username":username}))
    
   
    # if user:
    #     password_check = pwd_context.verify(password,user['password'])
    #     return password_check
    # else :
    #     False
        


@admin.post('/token')
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    # user = mydb.login.find({"username":username})

    # for i in user:
    #     username = i['username']
    #     password = i['password']
    #     print(username, password)

    if authenticate_user(username, password):
        return {"access_token": username, "token_type": "bearer"}

    else :
        raise HTTPException(status_code=400, detail="Incorrect username or password")

@admin.get('/') 
def home(token: str = Depends(oauth_scheme)):
    return {"token": token}
    


@admin.get('/user')
async def find_all_user(token: str = Depends(oauth_scheme)):
    """This function is querying all user account"""
    return usersEntity(mydb.login.find())


#================================================Chart of Account ==========================================
@admin.get("/chart-of-account")
async def find_chart_of_account():
    """This function is for querying chart of account"""
    return chartofAccounts(mydb.chart_of_account.find())