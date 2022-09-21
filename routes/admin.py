import json
from pyexpat import model
from fastapi import APIRouter, Body, HTTPException, Depends
from typing import Union
from datetime import datetime

from bson import ObjectId



from schemas.user import userEntity,usersEntity
from schemas.chartofAccount import chartofAccount,chartofAccounts
from schemas.bstype import bsType, bsTypes
from schemas.journalEntry import journalEntry,journalEntrys,journalEntryZambo,journalEntryZambos
from models.model import User, balansheetType, ChartofAccount,JournalEntry


from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from config.database import Base


from sqlalchemy.orm import Session


from pydantic import BaseModel
from datetime import datetime, date



from config.db import mydb
from config.database import engine,sessionLocal,Base

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

@admin.post('/sign-up')
def sign_up(fullname: str, username: str, password: str, status: str,created: Union[datetime, None] = Body(default=None),token: str = Depends(oauth_scheme)):
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
async def home(token: str = Depends(oauth_scheme)):
    return {"token": token}
    


@admin.get('/user')
async def find_all_user(token: str = Depends(oauth_scheme)):
    """This function is querying all user account"""
    return usersEntity(mydb.login.find())

#================================================balance sheet Type========================================
@admin.post("/insert-bstype")
def insert_bstype(item:balansheetType, token: str = Depends(oauth_scheme)):
    dataInsert = dict()
    dataInsert = {
        "bstype": item.bstype,
 
        }
    mydb.balansheetType.insert_one(dataInsert)
    return bsTypes(mydb.balansheetType.find())

@admin.get('/bstype')
async def get_all_bstye(token: str = Depends(oauth_scheme)):
    """This function is querying all user account"""
    return bsTypes(mydb.balansheetType.find())

@admin.put('/update-bstype{id}')
async def update_bstype(id,item:balansheetType):
    """This function is to update user info"""
    mydb.balansheetType.find_one_and_update({"_id":ObjectId(id)},{
        "$set":dict(item)
    })
    return bsTypes(mydb.balansheetType.find())


#================================================Chart of Account ==========================================
@admin.get("/chart-of-account")
async def find_chart_of_account():
    """This function is for querying chart of account"""
    return chartofAccounts(mydb.chart_of_account.find())


@admin.post("/insert-chart-of-account/")
def insert_chart_of_account(item:ChartofAccount):
    """This function is for querying chart of account"""
    dataInsert = dict()
    dataInsert = {
        "accountNum": item.accountNum,
        "accountTitle": item.accountTitle,
        "bsClass": item.bsClass,
        "user": "",
        "created": datetime.now()
 
        }
    mydb.chart_of_account.insert_one(dataInsert)
   

    return chartofAccounts(mydb.chart_of_account.find())


@admin.put('/update-chart-of-account/{id}')
async def update_user(id,item:ChartofAccount):
    """This function is to update user info"""
    mydb.chart_of_account.find_one_and_update({"_id":ObjectId(id)},{
        "$set":dict(item)
    })
    return chartofAccounts(mydb.chart_of_account.find({"_id":ObjectId(id)}))


#==============================================Insert Journal Entry================================
@admin.get("/show-journal-entry")
async def find_journal_entry(token: str = Depends(oauth_scheme)):
    """This function is for querying chart of account"""
    return journalEntrys(mydb.journal_entry.find())

@admin.delete('/delete-journal-entry/{id}')
def delete_journal_entry(id,token: str = Depends(oauth_scheme)):
    """This function is to delete journal Entry"""
    mydb.journal_entry.find_one_and_delete({"_id":ObjectId(id)})
    return  {'Messeges':'Data has been deleted'}


#==============================================Zamboanga Data===================================
@admin.get('/journal-entry-zambo/')
def get_journal_entry_zambo(token: str = Depends(oauth_scheme)):
    """This is for queryong journal entry for Zamboanga"""
    return journalEntryZambos(mydb.journal_entry_zambo.find())

@admin.delete('/delete-journal-entry-zambo/{id}')
def delete_journal_entry_zambo(id,token: str = Depends(oauth_scheme)):
    """This function is to delete journal Entry for Zambo"""
    mydb.journal_entry_zambo.find_one_and_delete({"_id":ObjectId(id)})
    return  {'Messeges':'Data has been deleted'}



#=============================================SQL Alchemy=======================================
class UserLogin(Base):
    __tablename__ = "admin_login"
    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String)
    username = Column(String)
    password_admin = Column(String)
    admin_status = Column(String)

class UserLogin_pydantic(BaseModel):
    
    id: int
    fullname = str
    username = str
    password_admin = str
    admin_status = str


@admin.get('/diesel-consuption')
async def get_diesel_consumption():
    """This function is for querying diesel Consumption"""
    
    return {"messege":'Hello World'}
    # return db.query(UserLogin)