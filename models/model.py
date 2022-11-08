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
    username: str
    date_update: date






   
#===============================================Surigao Database==============================
class DollarBill(BaseModel):
    """This is for Dollar Bill Pydantic Model"""
    trans_date: date
    equipment_id: str
    trackFactor: float
    no_trips: float
    usd_pmt: float  
    convertion_rate: float
    taxRate: float
    vat_output: float
    user:str
    date_credited: date


class InsertPesoBill(BaseModel):
    """This is for Surigao Peso Bill Pydantic Model"""
    trans_date: date
    equipment_id: str
    ore_owner: str
    trackFactor: float
    no_trips: float
    distance: float
    rate: float
    taxRate: float
    vat_output: float
    date_credited: date
    user: str
   

class Cashadvance(BaseModel):
    """This is for cash advance Pydantic Model"""

    employee_id : str
    lastname: str
    firstname: str
    ca_deduction:float




# ==========================================Zamboanga Table============================================

class Equipment(BaseModel):
    """This is for inserting Zamboanga Equipment true Pydatic Model"""

    equipment_id: str
    equipment_desc: str
    remarks: str

class Routes(BaseModel):
    """This is for inserting Routes Zamboanga Vitali Project"""
    routes_name: str
    distance: float
