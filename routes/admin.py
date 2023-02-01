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


from schemas.user import userEntity,usersEntity
from schemas.chartofAccount import chartofAccount,chartofAccounts
from schemas.bstype import bsType, bsTypes
from schemas.journalEntry import journalEntry,journalEntrys,journalEntryZambo,journalEntryZambos
from models.model import User, balansheetType, ChartofAccount,JournalEntry,UserLogin
from schemas.user import EmployeeuserEntity,EmployeeuserEntitys


from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# from config.database import Base


from sqlalchemy.orm import Session


import sqlalchemy
# from config.database import metadata,database

from authentication.utils import OAuth2PasswordBearerWithCookie


from pydantic import BaseModel
from datetime import datetime, date
from datetime import timedelta


from jose import jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
JWT_SECRET = 'myjwtsecret'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



from config.db import mydb
# from config.database import engine,sessionLocal,Base

admin = APIRouter()

# @admin.get('/')
# def home():
#     """This is for testing only"""
#     return {"Main":"This is Lenged"}


# def validateLogin(request:Request):
#     """This function is for Log In Authentication"""
    
#     try :
#         token = request.cookies.get('access_token')
#         if token is None:
#             raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail= "Not Authorized",
#             # headers={"WWW-Authenticate": "Basic"},
#             )
#         else:
#             scheme, _, param = token.partition(" ")
#             payload = jwt.decode(param, JWT_SECRET, algorithms=ALGORITHM)
        
#             username = payload.get("sub")
        

#             user =  mydb.login.find({"username":username})

#             if user is not None:

#                 return username

#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail= "Not Authorized",
#             # headers={"WWW-Authenticate": "Basic"},
#         )


#==================================================User Data =============================================
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)



from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")

# oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})

    
    return to_encode


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
def login(response:Response,form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    # # user = mydb.login.find({"username":username})

    # # for i in user:
    # #     username = i['username']
    # #     password = i['password']
    # #     print(username, password)

    # if authenticate_user(username, password):
    #     return {"access_token": username, "token_type": "bearer"}

    # else :
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")

    
    user = authenticate_user(username,password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username},
        expires_delta=access_token_expires,
    )

    data = {"sub": username}
    jwt_token = jwt.encode(data,SECRET_KEY,algorithm=ALGORITHM)
    response.set_cookie(key="access_token", value=f'Bearer {jwt_token}',httponly=True)
    
    return {"access_token": jwt_token, "token_type": "bearer"}
    # return {"access_token": access_token, "token_type": "bearer"}
    # return(access_token)

def get_user_from_token():

    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    username = payload.get("sub")
    return username
    # myresult = mydb.login.find({"username":username})

    # for i in myresult:
    #     user = i['username']
    #     print(user)

    # return user


@admin.get('/user')
async def find_all_user(token: str = Depends(oauth_scheme)):
    """This function is querying all user account"""
    return usersEntity(mydb.login.find())

#=============================================employee user frame========================================
@admin.get("/api-autocomplete-employee-user/")
def autocomplete(term: Optional[str],token: str = Depends(oauth_scheme)):
    """this is for auto complete of """
    items = EmployeeuserEntitys(mydb.employee_login.find({'fullname':{"$regex":term,'$options':'i'}}))

    suggestions = []
    for item in items:
        suggestions.append(item['fullname'])
    return suggestions

@admin.get('/api-get-employee-user/')
async def get_employee_user(fullname, token: str = Depends(oauth_scheme)):
    """This is for search of employee"""
    return  EmployeeuserEntitys(mydb.employee_login.find({'fullname':{"$regex":fullname,'$options':'i'}}))

@admin.put('/api-update-employee-user/')
async def update_employee_status(id,status:Optional[str],token: str = Depends(oauth_scheme)):
    """This function is to update user info"""
    mydb.employee_login.find_one_and_update({"_id":ObjectId(id)},{
        "$set":{
            "status":status
        }
    })
    return {'Messaeges':'Data has been updated'}


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


#==============================================Insert Journal Entry  Surigao================================
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
@admin.get('/api-view-journal-entry-zambo2/')
def get_journal_entry_zambo(token: str = Depends(oauth_scheme)):
    """This is for queryong journal entry for Zamboanga"""

    myresult  = mydb.journal_entry_zambo.find()
    journalData = [
            {
                
                "date_entry": item["date_entry"],
                "journal": item["journal"],
                "ref": item["ref"],
                "descriptions": item["descriptions"],
                "acoount_number": item["acoount_number"],
                "account_disc": item["account_disc"],
                "debit_amount": item["debit_amount"],
                "credit_amount": item["credit_amount"],
                

            }
            for item in myresult
        ]

    return journalData
    # return journalEntryZambos(mydb.journal_entry_zambo.find())



@admin.get('/journal-entry-zambo/')
def get_journal_entry_zambo(token: str = Depends(oauth_scheme)):
    """This is for queryong journal entry for Zamboanga"""
    return journalEntryZambos(mydb.journal_entry_zambo.find())

@admin.delete('/delete-journal-entry-zambo/{id}')
def delete_journal_entry_zambo(id,token: str = Depends(oauth_scheme)):
    """This function is to delete journal Entry for Zambo"""
    mydb.journal_entry_zambo.find_one_and_delete({"_id":ObjectId(id)})
    return  {'Messeges':'Data has been deleted'}


@admin.get('/api-trialbalance-surigao/')
def get_trialBalance_zambo(datefrom,dateto,token: str = Depends(oauth_scheme)):
    """This function is for querying Journal Entry for Zamboanga for Trial Balance"""
   
    date_time_obj_from = datetime.strptime(datefrom, '%Y-%m-%d')

    
    date_time_obj_to = datetime.strptime(dateto, '%Y-%m-%d')

    agg_result= mydb.journal_entry.aggregate(
        [
        {"$match":{'date_entry': {'$gte':date_time_obj_from, '$lte':date_time_obj_to},
           
        }},
        # {"$match": { "cut_off_period": date } },
        # {'$sort' : { '$meta': "textScore" }, '$account_disc': -1 },
        {"$group" : 
            {"_id" :  '$acoount_number',
            "accountName": {'$first':'$account_disc'},
            "totalDebit" : {"$sum" : '$debit_amount'},
            "totalCredit" : {"$sum" : '$credit_amount'},
            
            }},
        {'$sort':{'_id': 1}}
            
        ])
    agg_result_list = []
    for x in agg_result:

        accountNumber = x['_id']
        account_title = x['accountName']
        debit_amount = x['totalDebit']
        debit_amount2 = '{:.2f}'.format(debit_amount)
        credit_amount = x['totalCredit']
        credit_amount2 = '{:.2f}'.format(credit_amount)
        totalIncome =   float(credit_amount) - float(debit_amount)
        totalIncome2 = '{:,.2f}'.format(totalIncome)

        

        data={}   
        
        data.update({
            
            
            'acoount_number': accountNumber,
            'accountTitle': account_title,
            'debit_amount': debit_amount2,
            'credit_amount': credit_amount2,
            'totalAmount': totalIncome2,
        })

        agg_result_list.append(data)

    return agg_result_list



@admin.get('/api-trialbalance-zambo/')
def get_trialBalance_zambo(datefrom,dateto,token: str = Depends(oauth_scheme)):
    """This function is for querying Journal Entry for Zamboanga for Trial Balance"""
   
    date_time_obj_from = datetime.strptime(datefrom, '%Y-%m-%d')

    
    date_time_obj_to = datetime.strptime(dateto, '%Y-%m-%d')

    agg_result= mydb.journal_entry_zambo.aggregate(
        [
        {"$match":{'date_entry': {'$gte':date_time_obj_from, '$lte':date_time_obj_to},
           
        }},
        # {"$match": { "cut_off_period": date } },
        # {'$sort' : { '$meta': "textScore" }, '$account_disc': -1 },
        {"$group" : 
            {"_id" :  '$acoount_number',
            "accountName": {'$first':'$account_disc'},
            "totalDebit" : {"$sum" : '$debit_amount'},
            "totalCredit" : {"$sum" : '$credit_amount'},
            
            }},
        {'$sort':{'_id': 1}}
            
        ])
    agg_result_list = []
    for x in agg_result:

        accountNumber = x['_id']
        account_title = x['accountName']
        debit_amount = x['totalDebit']
        debit_amount2 = '{:.2f}'.format(debit_amount)
        credit_amount = x['totalCredit']
        credit_amount2 = '{:.2f}'.format(credit_amount)
        totalIncome =   float(credit_amount) - float(debit_amount)
        totalIncome2 = '{:,.2f}'.format(totalIncome)

        

        data={}   
        
        data.update({
            
            
            'acoount_number': accountNumber,
            'accountTitle': account_title,
            'debit_amount': debit_amount2,
            'credit_amount': credit_amount2,
            'totalAmount': totalIncome2,
        })

        agg_result_list.append(data)

    return agg_result_list






# admin_login = sqlalchemy.Table(
#     "admin_login",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("fullname", sqlalchemy.String),
#     sqlalchemy.Column("username", sqlalchemy.String),
#     sqlalchemy.Column("password_admin", sqlalchemy.String),
#     sqlalchemy.Column("admin_status", sqlalchemy.String),
# )

#=============================================SQL Alchemy=======================================

# @admin.get("/notes/", response_model=List[UserLogin])
# async def read_notes():
#     query = admin.select()
#     return await database.fetch_all(query)

from config.database import Database
Database.initialize()
@admin.get("/admin-user/")
def get_record():
    # allConsumption = db.query(query=f"SELECT * FROM diesel_consumption")
    
    # allconsuption2 = allConsumption['result']
    myresult = Database.select_all_from_dieselDB()
   

    agg_result_list = []
    for x in myresult:
        id = x[0]
        transaction_date = x[1]
        equipment_id = x[2]
        use_liter = x[4]
        use_liter2 = '{:,.2f}'.format(use_liter)
        price = x[5]
        amount = x[6]
        amount2 = '{:,.2f}'.format(amount)
        
        

        data={}   
        
        data.update({
            'id': id,
            'transaction_date': transaction_date,
            'equipment_id': equipment_id,
            'use_liter': use_liter2,
            'price': price,
            'amount': amount2,
        })

        agg_result_list.append(data)

    
    
    return  agg_result_list

from schemas.rizal import DieselConsumption,DieselConsumptions, RentalLists
from models.model import DieselConsumption
from config.database import Database
Database.initialize()
@admin.get("/diesel/")
def get_diesels():
    """This fucntion is for querying all diesel"""

    return DieselConsumptions(Database.select_all_from_dieselDB())

@admin.put('/api-update-diesel/{id}')
def update_diesel(id,item:DieselConsumption,token: str = Depends(oauth_scheme)):
    """This function is to update Diesel transactions info"""
    Database.update_one_diesel(transaction_date=item.transaction_date,
                            equipment_id=item.equipment_id,withdrawal_slip=item.withdrawal_slip,
                            use_liter=item.use_liter,price=item.price,
                            amount=item.amount,username=item.username,id=id)
                             
    return {"message":"data has been updated"}
@admin.get('/api-get-diesel-date/')
def get_diesel_withParams(datefrom,dateto,token: str = Depends(oauth_scheme)):
    """This function is for querying Diesel with parameters"""
    myresult = Database.select_diesel_withParams(datefrom=datefrom,dateto=dateto)

    query = []
    total_liters = 0
    total_amount = 0
    for i in myresult:
        use_liter = i[4]
        price = i[5]
        amount = i[6]
        total_liters+=use_liter
        total_amount+=amount


        use_liter2 = '{:,.2f}'.format(use_liter)
        total_liters2 = '{:,.2f}'.format(total_liters)
        price2 = '{:,.2f}'.format(price)
        amount2 = '{:,.2f}'.format(amount)
        total_amount2 = '{:,.2f}'.format(total_amount)

        data = {}
        data.update({
            "id": i[0],
            "transaction_date":i[1],
            "equipment_id": i[2],
            "withdrawal_slip": i[3],
            "use_liter": i[4],
            "total_liters": total_liters2,
            "price": price2,
            "amount": amount2,
            "total_amount": total_amount2
            
        })
        query.append(data)
    return query


@admin.get('/api-get-diesel-equipment/')
def get_diesel_withParams(datefrom,dateto,equipment_id,token: str = Depends(oauth_scheme)):
    """This function is for querying Diesel with parameters"""
    myresult = Database.select_diesel_equipID(datefrom=datefrom,dateto=dateto,
                                                equipment_id= equipment_id)

    query = []
    total_liters = 0
    total_amount = 0
    for i in myresult:
        use_liter = i[4]
        price = i[5]
        amount = i[6]
        total_liters+=use_liter
        total_amount+=amount


        use_liter2 = '{:,.2f}'.format(use_liter)
        total_liters2 = '{:,.2f}'.format(total_liters)
        price2 = '{:,.2f}'.format(price)
        amount2 = '{:,.2f}'.format(amount)
        total_amount2 = '{:,.2f}'.format(total_amount)

        data = {}
        data.update({
            "id": i[0],
            "transaction_date":i[1],
            "equipment_id": i[2],
            "withdrawal_slip": i[3],
            "use_liter": i[4],
            "total_liters": total_liters2,
            "price": price2,
            "amount": amount2,
            "total_amount": total_amount2
            
        })
        query.append(data)
    return query





#=============================================Rizal Equipment====================================
from schemas.rizal import CashAdvance,CashAdvances,EmployeeDetail,EmployeeDetails
from models.model import Cashadvance


@admin.get("/api-search-employee_by_empID/")
def get_equipment(term: Optional[str]):
    items = EmployeeDetails(Database.select_one_employee_with_empID(employee_id=term))
    return items

@admin.get("/api-search-employee_name/")
def autocomplete(term: Optional[str]):
    items = Database.select_one_employee(firstName=term)

    suggestions = []
    for item in items:
        suggestions.append(item[3])
    return suggestions

#=======================================Conpensation/Salary frame====================================
@admin.get('/api-get-comp13th/')
def compt13Month(date1,date2,department,token: str = Depends(oauth_scheme)):
    """This function is for computation of 13th month"""
    myresult = Database.computation13thMonth(date1=date1,date2=date2,department=department)

    test = []
    for i in myresult:
        totalAmount = (float(i[2]) + float(i[3]) + float(i[4]) + float(i[5]) + float(i[6]) + float(i[7]) +
                            float(i[8])) / 12
        totalAmount2 = '{:,.2f}'.format(totalAmount)
        data = {}
        data.update({
            "employee_id": i[0],
            "lastname":i[1],
            "fname": i[9],
            "department": i[10],
            "totalRegdays": i[2],
            "TotalRegSun": i[3],
            "TotalSpl": i[4],
            "Totallgl2": i[5],
            "Totalshoprate": i[6],
            "TotalproviRate": i[7],
            "TotalproviSun": i[8],
            "totalAmount": totalAmount2
        })
        test.append(data)
    return test

     # Compute the total amount for each employee
    # computations = map(
    #     lambda result: {
    #         "employee_id": result[0],
    #         "lastname": result[1],
    #         "fname": result[9],
    #         "totalRegdays": result[2],
    #         "TotalRegSun": result[3],
    #         "TotalSpl": result[4],
    #         "Totallgl2": result[5],
    #         "Totalshoprate": result[6],
    #         "TotalproviRate": result[7],
    #         "TotalproviSun": result[8],
    #         "totalAmount": '{:,.2f}'.format(
    #             sum([result[2], result[3], result[4], result[5], result[6], result[7], result[8]]) / 12
    #         )
    #     },
    #     results
    # )

    # # Return the computations
    # return computations

@admin.get('/api-select-employee-transaction/')
def get_employee_payroll_transactions(employee_id,token: str = Depends(oauth_scheme)):
    """This function is for displaying all reports or transaction for Employee  """
    myresult = Database.get_employee_cutoff_range(employee_id=employee_id)

    agg_result_list = []
    for x in myresult:
        transaction_date = x[0]
        employee_id = x[1]
        lastname = x[2]
        first_name = x[3]
        grosspay_save = x[4]
        netpay_save = x[5]

       
       
        grosspay_save2 = '{:,.2f}'.format(grosspay_save)
        netpay_save2 = '{:,.2f}'.format(netpay_save)
        
       
        

        data={}   
        
        data.update({
            
            "transaction_date": transaction_date,
            "employee_id": employee_id ,
            "lastname": lastname,
            "first_name": first_name,
            "grosspay_save": '{:,.2f}'.format(x[4]),
            "netpay_save": '{:,.2f}'.format(x[5]),
            "department": x[6]
           
        })

        agg_result_list.append(data)
    return (agg_result_list)



    # Create a list of dictionaries containing the transaction details
    # transactions = map(
    # lambda myresult: {
    #     "transaction_date": myresult[0],
    #     "employee_id": myresult[1],
    #     "lastname": myresult[2],
    #     "first_name": myresult[3],
    #     "grosspay_save": '{:,.2f}'.format(myresult[4]),
    #     "netpay_save": '{:,.2f}'.format(myresult[5]),
    #     "department": myresult[6]
    # },)

        



#=====================================Cash advances Frame============================================
@admin.post('/api-insert-cashadvance/')
def rizal_insert_cashAdnvances(item:Cashadvance,token: str = Depends(oauth_scheme)):
    """This function is for inserting Data or Cash Adnvances"""

    Database.insert_cash_advance(employee_id=item.employee_id,
                                    lastname=item.lastname,
                                    firstname=item.firstname,
                                    ca_deduction=item.ca_deduction)

    return {'Messeges':'Data has been save'}

@admin.get('/api-get-cashadvance/')
def get_cashadvances():
    """This function is for querying Cash advances"""
    return CashAdvances(Database.select_all_cashAdvanves())

@admin.delete('/api-delete-cash-advance/{id}')
def delete_employee(id,token: str = Depends(oauth_scheme)):
    """This function is to delete journal Entry"""
    Database.delete_one_from_cash(id=id)
    return  {'Messeges':'Data has been deleted'}

#===============================================Rizal Rental=======================================

@admin.get('/api-get-rental/')
def get_rental(datefrom,dateto,equipment_id,token: str = Depends(oauth_scheme)):
    """This is for querying rental true date transact"""

    myresult = Database.select_rental_with_parameters(datefrom=datefrom,dateto=dateto,equipment_id=equipment_id)
   

    agg_result_list = []
    rental_amount3 = 0
    for x in myresult:
        id = x[0]
        transaction_date = x[2]
        equipment_id = x[3]
        total_rental_hour = x[4]
        rental_rate = x[5]
        rental_amount = x[6]
        username = x[7]

        rental_amount3+=rental_amount
       
        rental_rate2 = '{:,.2f}'.format(rental_rate)
        rental_amount2 = '{:,.2f}'.format(rental_amount)
        rental_amount4 = '{:,.2f}'.format(rental_amount3)
        

        data={}   
        
        data.update({
            
            "id": id,
            "transaction_date": transaction_date ,
            "equipment_id": equipment_id,
            "total_rental_hour": total_rental_hour,
            "rental_rate": rental_rate2,
            "rental_amount": rental_amount2,
            "running_bal": rental_amount4,
            "username": username,
        })

        agg_result_list.append(data)
    return (agg_result_list)
    # return RentalLists(Database.select_rental_with_parameters(datefrom=datefrom,dateto=dateto))


@admin.get('/api-get-rental2/')
def get_rental(token: str = Depends(oauth_scheme)):
    """This is for querying rental true date transact"""

    myresult = Database.select_all_from_rentalDB()
   

    agg_result_list = []
    rental_amount3 = 0
    for x in myresult:
        id = x[0]
        transaction_date = x[2]
        equipment_id = x[3]
        total_rental_hour = x[4]
        rental_rate = x[5]
        rental_amount = x[6]
        rental_amount3+=rental_amount
        username = x[7]
       
        rental_rate2 = '{:,.2f}'.format(rental_rate)
        rental_amount2 = '{:,.2f}'.format(rental_amount)
        rental_amount4 = '{:,.2f}'.format(rental_amount3)
        

        data={}   
        
        data.update({
            
            "id": id,
            "transaction_date": transaction_date ,
            "equipment_id": equipment_id,
            "total_rental_hour": total_rental_hour,
            "rental_rate": rental_rate2,
            "rental_amount": rental_amount2,
            "running_bal": rental_amount4,
            "username": username,
        })

        agg_result_list.append(data)
        # print(agg_result_list)
    return (agg_result_list)
    # return RentalLists(Database.select_all_from_rentalDB())

@admin.delete('/api-delete-rental/{id}')
def delete_employee(id,token: str = Depends(oauth_scheme)):
    """This function is to delete journal Entry"""
    Database.delete_rental(id=id)
    return  {'Messeges':'Data has been deleted'}




#=============================================Surigao Database =====================================
from routes.client import login
# from routes.rizal_project import validateLogin
from config.surigaoDB import SurigaoDB
SurigaoDB.initialize()
from models.model import InsertPesoBill, DollarBill


#===============================================Surigao Peso==============================================

@admin.put('/api-update-dollarBill/{id}')
def update_dollarBill(id,item:DollarBill, token: str = Depends(oauth_scheme)):
    """This function is to update Diesel transactions info"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        print(payload)
    except Exception as e:
        print(e)
    date_credited = date.today() 
    SurigaoDB.update_one_dollarBill(trans_date=item.trans_date,
                                equipment_id=item.equipment_id,trackFactor=item.trackFactor,
                                no_trips=item.no_trips,usd_pmt=item.usd_pmt,
                                convertion_rate=item.convertion_rate,
                                taxRate=item.taxRate,vat_output=item.vat_output,user=item.user,
                                date_credited=date_credited,id=id)
                             
    return {"message":"data has been updated"}



#===============================================Surigao Peso==============================================

@admin.post('/api-insert-surigao-pesoBill/')
def insert_surigao_pesoBill(item:InsertPesoBill,token: str = Depends(oauth_scheme)):
    """This function is to update Diesel transactions info"""
    date_credited = date.today()
    SurigaoDB.insert_peso_production(trans_date=item.trans_date,
                                equipment_id=item.equipment_id,ore_owner=item.ore_owner,
                                trackFactor=item.trackFactor,no_trips=item.no_trips,
                                distance=item.distance,rate=item.rate,taxRate=item.taxRate,
                                vat_output=item.vat_output,date_credited=date_credited)
                             
    return {"message":"data has been updated"}

@admin.put('/api-update-pesoBill/{id}')
def update_dollarBill(id,item:InsertPesoBill, token: str = Depends(oauth_scheme)):
    """This function is to update Diesel transactions info"""
    
    try:
        # scheme, _, param = token.partition(" ")
        # payload = jwt.decode(param, JWT_SECRET, algorithms=ALGORITHM)
    
        # user = payload.get("sub")
        
        # payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        # user = payload.get('sub')
        # print(user)

        date_credited = date.today() 
        SurigaoDB.update_one_pesoBill(trans_date=item.trans_date,
                                    equipment_id=item.equipment_id,ore_owner=item.ore_owner,
                                    trackFactor=item.trackFactor,no_trips=item.no_trips,
                                    distance=item.distance,rate=item.rate,taxRate=item.taxRate,
                                    vat_output=item.vat_output,user=item.user,date_credited=date_credited,id=id)
                                
        return {"message":"data has been updated"}
        
    except Exception as e:
        print(e)
    



@admin.delete('/api-delete-surigao-pesoBill/{id}')
def delete_surigao_pesoBill(id,token: str = Depends(oauth_scheme)):
    """This function is to delete journal Entry for Zambo"""
    SurigaoDB.delete_one_from_peso(id)
    return  {'Messeges':'Data has been deleted'}



#============================================Vitali Zamboangao Project======================================
from config.zamboanga import ZamboangaDB
ZamboangaDB.initialize()
from models.model import Equipment,Routes, Hauling,Vitalidiesel

@admin.post('/api-add-equipment/')
def add_equipment(items: Equipment, token: str = Depends(oauth_scheme)):
    """This function is for posting equipment"""

    ZamboangaDB.insert_equipment(equipment_id=items.equipment_id,
                                    equipment_desc=items.equipment_desc,
                                    remarks=items.remarks )
    return {'Messege': ' Data Has been Save'}

@admin.get('/api-get-equipment/')
def get_equipment(token: str=Depends(oauth_scheme)):
    """This function is for querying all Equipment"""
    myresult = ZamboangaDB.select_all_equipment()

    agg_result_list = []
    
    for x in myresult:
        id = x[0]
        equipment_id = x[1]
        equipment_desc = x[2]
        remarks = x[3]
       

        data={}   
        
        data.update({
            
            "id": id,
            "equipment_id": equipment_id ,
            "equipment_desc": equipment_desc,
            "remarks": remarks
          
        })

        agg_result_list.append(data)
        # print(agg_result_list)
    return agg_result_list



@admin.put('/api-update-equipment/{id}')
def update_equipment(id,item:Equipment,token: str = Depends(oauth_scheme)):
    """This function is to update equipment """
    ZamboangaDB.update_equipment(id=id,equipment_id=item.equipment_id,
                                    equipment_desc=item.equipment_desc,
                                    remarks=item.remarks)
    return  {'Messeges':'Data has been updated'}

@admin.delete('/api-delete-equipment/{id}')
def delete_equipment(id,token: str = Depends(oauth_scheme)):
    """This function is to delete equipment"""
    ZamboangaDB.delete_equipment(id=id)
    return  {'Messeges':'Data has been deleted'}

@admin.get("/api-search-equipment/")
def autocomplete_equipment(id):
    items = ZamboangaDB.select_equipment(id=id)


    agg_result_list = []
    
    for x in items:
        id = x[0]
        equipment_id = x[1]
        equipment_desc = x[2]
        remarks = x[3]
       

        data={}   
        
        data.update({
            
            "id": id,
            "equipment_id": equipment_id ,
            "equipment_desc": equipment_desc,
            "remarks": remarks
          
        })

        agg_result_list.append(data)
        # print(agg_result_list)
    return (agg_result_list)

@admin.get("/api-search-autocomplete-equipment/")
def autocomplete_equipmentID(term: Optional[str]):
    items = ZamboangaDB.select_equipmentID(equipment_id=term)

    suggestions = []
    for item in items:
        suggestions.append(item[1])
        
    return suggestions


#============================================Routes============================================
@admin.post('/api-add-routes/')
def add_equipment(items: Routes, token: str = Depends(oauth_scheme)):
    """This function is for posting routes"""

    ZamboangaDB.insert_routes(routes_name=items.routes_name,
                                distance=items.distance)
    return {'Messege': 'Has been Save'}

@admin.get('/api-get-routes/')
def get_routes(token: str=Depends(oauth_scheme)):
    """This function is for querying all Equipment"""
    myresult = ZamboangaDB.select_all_routes()

    agg_result_list = []
    
    for x in myresult:
        id = x[0]
        routes_name = x[1]
        distance = x[2]
    
        data={}   
        
        data.update({
            
            "id": id,
            "routes_name": routes_name ,
            "distance": distance,
            
          
        })

        agg_result_list.append(data)
        # print(agg_result_list)
    return (agg_result_list)


@admin.get("/api-search-routes/")
def autocomplete_routes(term: Optional[str]):
    items = ZamboangaDB.select_routes(routes_name=term)

    suggestions = []
    for item in items:
        suggestions.append(item[1])
        
    return suggestions


@admin.get("/api-search-distance/")
def autocomplete_routes_distance(term: Optional[str]):
    items = ZamboangaDB.select_routes(routes_name=term)

    suggestions = []
    for item in items:
        suggestions.append(item[2])
        
    return suggestions


#=======================================Vitali Hauling=====================================
@admin.post('/api-add-hauling/')
def add_equipment(items: Hauling, token: str = Depends(oauth_scheme)):
    """This function is for posting routes"""

   
    
    dateToday = date.today()

    ZamboangaDB.insert_hauling(trans_date=items.trans_date,equipment_id=items.equipment_id,
                                routes=items.routes,distance=items.distance,
                                trackFactor=items.trackFactor,no_trips=items.no_trips,
                                volume=items.volume,rate=items.rate,taxRate=items.taxRate,
                                amount=items.amount,vat_output=items.vat_output,
                                net_of_vat=items.net_of_vat,user=items.user,date_credited=dateToday)
    return {'Messege': 'Has been Save'}


@admin.get('/api-get-haulings/')
def get_hauling(token: str=Depends(oauth_scheme)):
    """This function is for querying all Hauling"""
    myresult = ZamboangaDB.select_all_hauling()

    agg_result_list = []
    
    for x in myresult:
        id = x[0]
        trans_date = x[1]
        equipment_id = x[2]
        routes = x[3]
        distance = x[4]
        trackFactor = x[5]
        no_trips = x[6]
        volume = x[7]
        rate = x[8]
        taxRate = x[9]
        amount = x[10]
        vat_output = x[11]
        net_of_vat = x[12]
        user = x[13]
        date_updated = x[14]
        date_credited = x[15]
    
        data={}   
        
        data.update({
            
            "id": id,
            "trans_date": trans_date ,
            "equipment_id": equipment_id,
            "routes": routes,
            "distance": distance,
            "trackFactor": trackFactor,
            "no_trips": no_trips,
            "volume": volume,
            "rate": rate,
            "taxRate": taxRate,
            "amount": amount,
            "vat_output": vat_output,
            "net_of_vat": net_of_vat,
            "user": user,
            "date_updated": date_updated,
            "date_credited": date_credited,
          
        })

        agg_result_list.append(data)
        # print(agg_result_list)
    return agg_result_list

@admin.get('/api-get-haulings-with-params/')
def get_hauling_date_equipmentID(datefrom,dateto,equipment_id,token: str=Depends(oauth_scheme)):
    """This function is for querying all Hauling"""
    myresult = ZamboangaDB.select_hauling_withParams(datefrom=datefrom,dateto=dateto,equipment_id=equipment_id)

    agg_result_list = []
    
    for x in myresult:
        id = x[0]
        trans_date = x[1]
        equipment_id = x[2]
        routes = x[3]
        distance = x[4]
        trackFactor = x[5]
        no_trips = x[6]
        volume = x[7]
        rate = x[8]
        taxRate = x[9]
        amount = x[10]
        vat_output = x[11]
        net_of_vat = x[12]
        user = x[13]
        date_updated = x[14]
        date_credited = x[15]
    
        data={}   
        
        data.update({
            
            "id": id,
            "trans_date": trans_date ,
            "equipment_id": equipment_id,
            "routes": routes,
            "distance": distance,
            "trackFactor": trackFactor,
            "no_trips": no_trips,
            "volume": volume,
            "rate": rate,
            "taxRate": taxRate,
            "amount": amount,
            "vat_output": vat_output,
            "net_of_vat": net_of_vat,
            "user": user,
            "date_updated": date_updated,
            "date_credited": date_credited,
          
        })

        agg_result_list.append(data)
        # print(agg_result_list)
    return agg_result_list


@admin.get('/api-get-hauling-with-id/')
def get_hauling_date_equipmentID(id,token: str=Depends(oauth_scheme)):
    """This function is for querying all Hauling"""
    myresult = ZamboangaDB.select_hauling_id(id=id)

    agg_result_list = []
    
    for x in myresult:
        id = x[0]
        trans_date = x[1]
        equipment_id = x[2]
        routes = x[3]
        distance = x[4]
        trackFactor = x[5]
        no_trips = x[6]
        volume = x[7]
        rate = x[8]
        taxRate = x[9]
        amount = x[10]
        vat_output = x[11]
        net_of_vat = x[12]
        user = x[13]
        date_updated = x[14]
        date_credited = x[15]
    
        data={}   
        
        data.update({
            
            "id": id,
            "trans_date": trans_date ,
            "equipment_id": equipment_id,
            "routes": routes,
            "distance": distance,
            "trackFactor": trackFactor,
            "no_trips": no_trips,
            "volume": volume,
            "rate": rate,
            "taxRate": taxRate,
            "amount": amount,
            "vat_output": vat_output,
            "net_of_vat": net_of_vat,
            "user": user,
            "date_updated": date_updated,
            "date_credited": date_credited,
          
        })

        agg_result_list.append(data)
        # print(agg_result_list)
    return agg_result_list



@admin.put('/api-update-hauling/{id}')
def update_hauling(id,items:Hauling,token: str = Depends(oauth_scheme)):
    """This function is to update equipment """

    dateToday = date.today()
    

    ZamboangaDB.update_hauling(id=id,trans_date=items.trans_date,equipment_id=items.equipment_id,
                        routes=items.routes,distance=items.distance,
                        trackFactor=items.trackFactor,no_trips=items.no_trips,volume=items.volume,
                        rate=items.rate,taxRate=items.taxRate,amount=items.amount,vat_output=items.vat_output,
                        net_of_vat=items.net_of_vat,user=items.user,date_updated=dateToday)

    return  {'Messeges':'Data has been updated'}


@admin.get('/api-get-per-equipment-sum/')
def get_sum_per_equipment(equipment_id,datefrom,dateto, token: str = Depends(oauth_scheme)):
    """This function is to get data sum of per Equipment"""
    myresult = ZamboangaDB.select_hauling_sum_per_equipment(datefrom=datefrom,dateto=dateto,equipment_id=equipment_id)

    agg_result_list = []
    
    for x in myresult:
        
        equipment_id = x[0]
        routes = x[1]
        no_trips = x[2]
        volume = x[3]
        amount = x[4]
        net_of_vat = x[5]
       
    
        data={}   
        
        data.update({
            
           
            "equipment_id": equipment_id,
            "routes": routes,
            "no_trips": no_trips,
            "volume": volume,
            "amount": amount,
            "net_of_vat": net_of_vat,
           
          
        })

        agg_result_list.append(data)
        # print(agg_result_list)
    return agg_result_list


    


@admin.delete('/api-delete-hauling/{id}')
def delete_hauling(id,token: str = Depends(oauth_scheme)):
    """This function is to delete equipment"""
    ZamboangaDB.delete_hauling(id=id)
    return  {'Messeges':'Data has been deleted'}


#==========================================This is for inserting Diesel=======================================
@admin.post('/api-insert-vitali-diesel/')
def insert_diesel(items:Vitalidiesel, token: str = Depends(oauth_scheme)):
    """This function is for inserting Diesel for Vitali Project"""
    dateToday = date.today()
    ZamboangaDB.insert_diesel(trans_date=items.trans_date,equipment_id=items.equipment_id,
                                withdrawal_slip=items.withdrawal_slip,liters=items.liters,
                                price=items.price,amount=items.amount,user=items.user,date_credited=dateToday)
    return {'Measseges': 'Data has been inserted'}


@admin.get('/api-search-all-diesel/')
async def get_all_diesel(equipment_id,datefrom,dateto,token: str = Depends(oauth_scheme)):
    """This function is for querying all diesel """

    myresult = ZamboangaDB.select_all_diesel_with_equipmentID(datefrom=datefrom,
                                        dateto=dateto,equipment_id=equipment_id)

    agg_result_list = []
    
    for x in myresult:
        
        trans_id = x[0]
        trans_date = x[1]
        equipment_id = x[2]
        withdrawal_slip = x[3]
        liters = x[4]
        price = x[5]
        amount = x[6]
       
       
    
        data={}   
        
        data.update({
            
            "trans_id": trans_id,
            "trans_date": trans_date,
            "equipment_id": equipment_id,
            "withdrawal_slip": withdrawal_slip,
            "liters": liters,
            "price": price,
            "amount": amount,
        
        })

        agg_result_list.append(data)
        # print(agg_result_list)
    return agg_result_list

@admin.delete('/api-delete-diesel/{id}')
def delete_diesel(id,token: str = Depends(oauth_scheme)):
    """This function is to delete equipment"""
    ZamboangaDB.delete_diesel(id=id)
    return  {'Messeges':'Data has been deleted'}
   





    

    