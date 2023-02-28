import json
from lib2to3.pgen2 import token
from pyexpat import model
from re import I


from authentication.utils import OAuth2PasswordBearerWithCookie

from fastapi import APIRouter, Body, HTTPException, Depends, Request, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Union, List
from datetime import datetime

from bson import ObjectId
from typing import Optional


from datetime import timedelta, datetime,date


from models.model import EmployeeUser

from schemas.user import usersEntity


from config.db import mydb


from jose import jwt

JWT_SECRET = 'myjwtsecret'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

employee_user = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")



from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")



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
        
            user =  usersEntity(mydb.employee_login.find({"username":username}))
            

            
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

#=========================================Equipment transactions====================================
from config.zamboanga import ZamboangaDB
ZamboangaDB.initialize()
from models.model import Equipment,Routes, Hauling,Vitalidiesel


@employee_user.get("/employee-transaction-zambo/", response_class=HTMLResponse)
async def api_login(request: Request, username: str = Depends(EmployeevalidateLogin)):
    return templates.TemplateResponse("employee/vitali_employee_transact.html", {"request":request}) 


@employee_user.post('/api-add-equipment-employee/')
def add_equipment(items: Equipment, username: str = Depends(EmployeevalidateLogin)):
    """This function is for posting equipment"""

    ZamboangaDB.insert_equipment(equipment_id=items.equipment_id,
                                    equipment_desc=items.equipment_desc,
                                    remarks=items.remarks )
    return {'Messege': ' Data Has been Save'}

@employee_user.get('/api-get-equipment-employee/')
def get_equipment(username: str = Depends(EmployeevalidateLogin)):
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
    return (agg_result_list)


#=================================================Employee Rizal Transaction ======================================

@employee_user.get("/employee-rizal-equipment-rental/", response_class=HTMLResponse)
async def api_login(request: Request, username: str = Depends(EmployeevalidateLogin)):
    return templates.TemplateResponse("employee/rizal_employee_trans.html", {"request":request}) 


from config.models import (insertEquipmentRental,getallRental,
                            insertRizalDiesel,diesel_consumption,getallDiesel)
from models.model import RizalRental,RizalDiesel
@employee_user.post("/api-insert-employee-rizal-rental/")
async def insertRental(items:RizalRental,username: str = Depends(EmployeevalidateLogin)):
    """This function is to update employee Details"""
    today = datetime.now()
    insertEquipmentRental(transaction_date=items.transaction_date,equipment_id=items.equipment_id,
                            total_rental_hour=items.total_rental_hour,rental_rate=items.rental_rate,
                            rental_amount=items.rental_amount, username=username,date_update=today)


    return  {'Messeges':'Data has been Save'} 


@employee_user.get("/api-get-rental-rizal-employee_login/")
async def getAllRentalRizal(datefrom,dateto,equipment_id,username: str = Depends(EmployeevalidateLogin)):
    """This function is for testing"""


    data = getallRental(datefrom=datefrom,dateto=dateto,equipment_id=equipment_id)

    rentalData = []
    totalAmount = 0
    for i in data:
       
        totalAmount+=i.rental_amount
        

        data={}   
        
        data.update({
                "id": i.id,
                "transaction_date": i.transaction_date,
                "equipment_id": i.equipment_id,
                "total_rental_hour": "{:,.2f}".format(i.total_rental_hour),
                "rental_rate": "{:,.2f}".format(i.rental_rate),
                "rental_amount": "{:,.2f}".format(i.rental_amount),
                "username": i.username,
                "totalAmount": "{:,.2f}".format(totalAmount),
                "date_update": i.date_update,
        })

        rentalData.append(data)

    return rentalData


@employee_user.post("/api-insert-rizalDiesel-employeeLogin/")
async def insertRental(items: RizalDiesel,username: str = Depends(EmployeevalidateLogin)):
    """This function is to update employee Details"""
    today = datetime.now()
    insertRizalDiesel(transaction_date=items.transaction_date,equipment_id=items.equipment_id,
                            withdrawal_slip=items.withdrawal_slip,
                            use_liter=items.use_liter,price=items.price,
                            amount=items.amount, username=username)

    return  {'Messeges':'Data has been Save'} 

@employee_user.get("/api-get-diesel-rizal-employeeLogin/")
async def getAllDieselRizal(datefrom,dateto,equipment_id:Optional[str],username: str = Depends(EmployeevalidateLogin)):
    """This function is for testing"""


    data = getallDiesel(datefrom=datefrom,dateto=dateto,equipment_id=equipment_id)

    rentalData = []
    totalAmount = 0
    for i in data:
       
        totalAmount+=i.amount
        

        data={}   
        
        data.update({
                "id": i.id,
                "transaction_date": i.transaction_date,
                "equipment_id": i.equipment_id,
                "withdrawal_slip": i.withdrawal_slip,
                "use_liter": "{:,.2f}".format(i.use_liter),
                "price": "{:,.2f}".format(i.price),
                "amount": "{:,.2f}".format(i.amount),
                "totalAmount": "{:,.2f}".format(totalAmount),
                
        })

        rentalData.append(data)

    return rentalData


#============================================Rizal Tonnage Frame=========================================
from config.models import insertTonnageRizal,getallTonnage
from models.model import RizalTonnagehaul
@employee_user.post("/api-insert-rizalTonnage-employeeLogin/")
async def insertTonnage(items: RizalTonnagehaul,username: str = Depends(EmployeevalidateLogin)):
    """This function is to update employee Details"""
    today = datetime.now()
    insertTonnageRizal(transDate=items.transDate,equipment_id=items.equipment_id,
                       tripTicket=items.tripTicket,totalTrip=items.totalTrip, totalTonnage=items.totalTonnage,
                       rate=items.rate,amount=items.amount,driverOperator=items.driverOperator,
                       user=username,date_credited=today)
    print(insertTonnageRizal())
    return  {'Messeges':'Data has been Save'}


@employee_user.get("/api-get-tonnage-rizal-employeeLogin/")
async def getAllTonnageRizal(datefrom,dateto,equipment_id:Optional[str],username: str = Depends(EmployeevalidateLogin)):
    """This function is for testing"""


    data = getallTonnage(datefrom=datefrom,dateto=dateto,equipment_id=equipment_id)

    rentalData = []
    totalAmount = 0
    for i in data:
       
        totalAmount+=i.amount
        

        data={}   
        
        data.update({
                "id": i.id,
                "transDate": i.transDate,
                "equipment_id": i.equipment_id,
                "tripTicket": i.tripTicket,
                "totalTrip": "{:,.2f}".format(i.totalTrip),
                "totalTonnage": "{:,.2f}".format(i.totalTonnage),
                "rate": "{:,.2f}".format(i.rate),
                "amount": "{:,.2f}".format(i.amount),
                "totalAmount": "{:,.2f}".format(totalAmount),
                "driverOperator": i.driverOperator,
        })

        rentalData.append(data)

    return rentalData
#===============================================Cost Frame Function =======================================

from config.models import insertCost,select_cost
from models.model import Cost
@employee_user.post("/api-insert-rizal-cost-employeeLogin/")
async def insertCostapi(items:Cost,username: str = Depends(EmployeevalidateLogin)):
    """This function is to update employee Details"""
    today = datetime.now()

    insertCost(transDate=items.transDate,equipment_id=items.equipment_id,salaries=items.salaries,
                    fuel=items.fuel,oil_lubes=items.oil_lubes, 
                    mechanicalSupplies=items.mechanicalSupplies,
                    repairMaintenance=items.repairMaintenance,meals=items.meals,
                    transpo=items.transpo,tires=items.tires,amortization=items.amortization,
                    others=items.others, totalAmount=items.totalAmount,user=username,date_created=today)

    return  {'Messeges':'Data has been Save'}


@employee_user.get("/api-get-rizal-cost-employeeLogin/")
async def get_cost(datefrom,dateto,equipment_id,username: str = Depends(EmployeevalidateLogin)):
    """This function is to update employee Details"""
    results = select_cost(datefrom=datefrom,dateto=dateto,equipment_id=equipment_id)

    costData = [
        
            {
                "id": x.id,
                "transDate": x.transDate,
                "equipment_id": x.equipment_id,
                "salaries": "{:,.2f}".format(x.salaries),
                "fuel": "{:,.2f}".format(x.fuel),
                "oil_lubes": "{:,.2f}".format(x.oil_lubes),
                "mechanicalSupplies": "{:,.2f}".format(x.mechanicalSupplies),
                "repairMaintenance": "{:,.2f}".format(x.repairMaintenance),
                "meals": "{:,.2f}".format(x.meals),
                "transpo": "{:,.2f}".format(x.transpo),
                "tires": "{:,.2f}".format(x.tires),
                "amortization": "{:,.2f}".format(x.amortization),
                "others": "{:,.2f}".format(x.others),
                "totalAmount": "{:,.2f}".format(x.totalAmount),
            
            }
            for x in results
        ]
    

    return costData


