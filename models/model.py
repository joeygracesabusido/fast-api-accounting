from lib2to3.pytree import Base
from pydantic import BaseModel
from datetime import datetime, date

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# from config.database import Base

class User(BaseModel):
    fullname: str
    username: str
    password: str
    status: str
    created: datetime

class balansheetType(BaseModel):
    bstype: str

class ChartofAccount(BaseModel):
    accountNum: str
    accountTitle: str
    bsClass: str
    user: str
    created: datetime

class JournalEntry(BaseModel):
    date_entry: date
    journal: str
    ref: str
    descriptions: str
    acoount_number: str
    account_disc: str
    bsClass: str
    debit_amount: float
    credit_amount: float
    due_date_apv: date
    terms_days: int
    supplier_Client: str
    user: str
    created:datetime

#=============================================SQL Alchemy================================================

class UserLogin(BaseModel):
    
    id: int
    fullname = str
    username = str
    password_admin = str
    admin_status = str
    



#==============================================Rizal=======================================================
class DieselConsumption(BaseModel):
   
    transaction_date: date
    equipment_id: str
    withdrawal_slip: str
    use_liter: float
    price: float
    amount: float
   

