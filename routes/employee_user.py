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

# from config.db import mydb
from config.mongodb_con import create_mongo_client
mydb = create_mongo_client()

# from config.db import worker

from config.models import Dieselrizal_class


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
            response = templates.TemplateResponse("login_api.html", {"request":request,"msg":msg})
            response.set_cookie(key="access_token", value=f'Bearer {token}',httponly=True)
            return response
            
           

        else :
            msg.append('Incorrect username or password')
            # raise HTTPException(status_code=400, detail="Incorrect username or password")
            return templates.TemplateResponse("login_api.html", {"request":request,"msg":msg})
    except:
        errors.append('Something wrong')
        return templates.TemplateResponse("login_api.html", {"request":request,"msg":msg})

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
        
        mydb.employee_login.create_index([("username", 1)], unique=True)
        mydb.employee_login.insert_one(dataInsert)
    
    except Exception as ex:
        error_message = f"Error due to: {str(ex)}"
        return {"error": error_message}
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
from config.models import getEquipmentRizal, getallRentalCheck
@employee_user.get("/employee-rizal-equipment-rental/", response_class=HTMLResponse)
async def api_login(request: Request, username: str = Depends(EmployeevalidateLogin)):
    """This function is to display List of Equipment to Front end for Selecting Equipment"""
    # result = getEquipmentRizal()
    
    
    # equipmentData = [
        
    #         {
    #             "id": i.id,
    #             "equipment_id": i.equipment_id,
               
               
    #         }
    #        for i in result
    #     ]
    
    
    return templates.TemplateResponse("employee/rizal_employee_trans.html", 
                                        {"request":request}) 


from config.models import (insertEquipmentRental,getallRental,
                            insertRizalDiesel,diesel_consumption,getallDiesel,getAllDiesel_checking,
                            select_rizalEquipment,rentalSumRizal,dieselSumRizal,getChartRental
                            ,getMonthlyRental,updateTonnage,insert_invetory_item)
from models.model import RizalRental,RizalDiesel,InventoryItemsModel
@employee_user.post("/api-insert-employee-rizal-rental/")
async def insertRental(items:RizalRental,username: str = Depends(EmployeevalidateLogin)):
    """This function is to update employee Details"""
    today = datetime.now()
    insertEquipmentRental(transaction_date=items.transaction_date,equipment_id=items.equipment_id,
                            total_rental_hour=items.total_rental_hour,rental_rate=items.rental_rate,
                            rental_amount=items.rental_amount, username=username,date_update=today,
                            eur_form=items.eur_form)


    return  {'Messeges':'Data has been Save'} 

@employee_user.get("/api-get-rental-rate-employeLogin/")
async def get_equipmentRate(equipment_id = Optional[str],username: str = Depends(EmployeevalidateLogin)):
    """This function is to query equipment Rental Rate """
    result = select_rizalEquipment(equipment_id=equipment_id)
    
    
    equipmentData = [
        
            {
                "id": i.id,
                "equipment_id": i.equipment_id,
                "rental_rate": i.rental_rate
               
            }
           for i in result
        ]
    
    return equipmentData

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
                "eur_form": i.eur_form,
                "equipment_id": i.equipment_id,
                "total_rental_hour": "{:.2f}".format(i.total_rental_hour),
                "rental_rate": "{:.2f}".format(i.rental_rate),
                "rental_amount": "{:.2f}".format(i.rental_amount),
                "username": i.username,
                "totalAmount": "{:,.2f}".format(totalAmount),
                "date_update": i.date_update,
        })

        rentalData.append(data)

    return rentalData

@employee_user.get("/api-get-rentalSum-rizal-employeeLogin/")
async def getRentalSumRizal(datefrom,dateto,equipment_id:Optional[str],username: str = Depends(EmployeevalidateLogin)):
    """This function is for testing"""


    data = rentalSumRizal(datefrom=datefrom,dateto=dateto,equipment_id=equipment_id)

    rentalData = []

    for i in data:
       
        # totalAmount+=i.amount
        totalHours = i.totalHours
        rentalRate = i.rental_rate
        totalAmount = float(totalHours) * float(rentalRate)

        data={}   
        
        data.update({
                "equipmentId": i.equipment_id,
                "totalHours":  "{:,.2f}".format(i.totalHours),
                "rentalRate": "{:,.2f}".format(i.rental_rate),
                "totalAmount":  "{:,.2f}".format(totalAmount),
                "totalAmount2":  "{:.2f}".format(totalAmount)
        })

        rentalData.append(data)

    return rentalData


@employee_user.get("/api-get-rentalCheck-employeLogin/")
async def get_rentalSearch(dateSearch,equipment_id,
                            eur_form,total_rental_hour,username: str = Depends(EmployeevalidateLogin)):
    """This function is to query equipment Rental Rate """
    result = getallRentalCheck(dateSearch=dateSearch,equipment_id=equipment_id,
                                    eur_form=eur_form,total_rental_hour=total_rental_hour)
    
    
    rentalData = [
        
            {
                "transaction_date": i.transaction_date,
                "equipment_id": i.equipment_id,
                "eur_form": i.eur_form,
                "total_rental_hour": i.total_rental_hour
               
            }
           for i in result
        ]
    
    
    return rentalData

@employee_user.get("/api-get-rentalChart-employeLogin/")
async def get_rentalSearch(datefrom,dateto,username: str = Depends(EmployeevalidateLogin)):
    """This function is to query equipment Rental Rate """
    result = getChartRental(datefrom=datefrom,dateto=dateto)
    
    
    rentalData = [
        
            {
                "transaction_date": i.transaction_date,
                "totalHours": i.totalHours,
               
               
            }
           for i in result
        ]
    
    
    return rentalData


@employee_user.get("/api-get-rentalChartMonthly-employeLogin/")
async def get_rentalSearch(username: str = Depends(EmployeevalidateLogin)):
    """This function is to query equipment Rental Rate """
    result = getMonthlyRental()
    
    
    rentalData = [
        
            {
                "month_year": i.month_year,
                "total_hours": i.total_hours,
               
               
            }
           for i in result
        ]
    
    
    return rentalData


from config.models import updateRentalRizal,getallRental_id
@employee_user.get("/update-rental-rizal-employeeLogin/{id}", response_class=HTMLResponse)
async def get_costData_id(id,request: Request):

    result = getallRental_id(id=id)
    
    
    rentalData = [
        
            {
                "id": i.id,
                "transaction_date": i.transaction_date,
                "eur_form": i.eur_form,
                "equipment_id": i.equipment_id,
                "total_rental_hour": i.total_rental_hour,
                "rental_rate": i.rental_rate,
                "rental_amount": i.rental_amount,
                "username": i.username,
                "date_update": i.date_update,
            
            }
           for i in result
        ]
    
   
   
    return templates.TemplateResponse("employee/updateRental_rizal.html",{"request":request,"rentalData":rentalData})

from models.model import RizalRental
@employee_user.put("/api-update-rental-rizal-employeeLogin/{id}")
async def updateRizalRental(id,items:RizalRental,username: str = Depends(EmployeevalidateLogin)):
    """This function is to update Cost"""
    today = datetime.now()

    updateRentalRizal(transaction_date=items.transaction_date,equipment_id=items.equipment_id,
                            total_rental_hour=items.total_rental_hour, rental_rate=items.rental_rate,rental_amount=items.rental_amount,
                             username=username,date_update=today,eur_form=items.eur_form, id=id)

    return  {'Messeges':'Data has been Updated'}





#==============================================Diesel Rizal Transaction=======================================

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


@employee_user.get("/api-get-rizal-dieselCheck-employeeLogin/")
async def get_dieselChecker(transaction_date,equipment_id:str=[Optional],withdrawal_slip:str =[Optional],
                            username: str = Depends(EmployeevalidateLogin)):
    """This function is to update employee Details"""
    results = getAllDiesel_checking(transaction_date=transaction_date,equipment_id=equipment_id,
                                        withdrawal_slip=withdrawal_slip)

    DieselData = [
        
            {
               "id": i.id,
                "transaction_date": i.transaction_date,
                "equipment_id": i.equipment_id,
                "withdrawal_slip": i.withdrawal_slip,
            
            }
            for i in results
        ]
    

    return DieselData


@employee_user.get("/api-get-rizal-sumDiesel-employeeLogin/")
async def get_dieselSumRizal(datefrom,dateto,equipment_id: Optional[str],
                            username: str = Depends(EmployeevalidateLogin)):
    """This function is to update employee Details"""
    results = dieselSumRizal(datefrom=datefrom,dateto=dateto,equipment_id=equipment_id)

    DieselData = [
        
            {
               
               "equipment_id": i.equipment_id,
                "use_liter": i.use_liter,
                "amount": "{:,.2f}".format(i.amount),
                "amount2": "{:.2f}".format(i.amount)
            }
            for i in results
        ]
    

    return DieselData


@employee_user.get("/update-diesel-employeeLogin/{id}", response_class=HTMLResponse)
async def get_updateDiesel(request:Request,id, username: str = Depends(EmployeevalidateLogin)):
    """This function is for dispalying Diesel Transaction using ID"""
    myresult = Dieselrizal_class.getdieselRizalID(id=id)
   
    
    agg_result_list = []
    
    for i in myresult:
        id_update = i.id,
        transaction_date = i.transaction_date
        equipment_id = i.equipment_id
        withdrawal_slip = i.withdrawal_slip
        use_liter = i.use_liter
        price = i.price
        amount = i.amount
        
        
        

        data={}   
        
        data.update({
            'id': id,
            'transaction_date': transaction_date,
            'equipment_id': equipment_id,
            'withdrawal_slip': withdrawal_slip,
            'use_liter': use_liter,
            'price': price,
            'amount': amount,
        
        })

        agg_result_list.append(data)

    # return agg_result_list

    return  templates.TemplateResponse("employee/updateDieselRizal.html", 
                                        {"request":request,"agg_result_list":agg_result_list
                                        })

@employee_user.put("/api-update-diesel-employeeLogin2/{id}")
async def updateDieselRizalEmployeeLogin(id,items: RizalDiesel,username: str = Depends(EmployeevalidateLogin)):
    """This function is to update employee Details"""
    
    Dieselrizal_class.updateDieselRizal_emp(transaction_date=items.transaction_date,equipment_id=items.equipment_id,
                                            withdrawal_slip=items.withdrawal_slip,use_liter=items.use_liter,
                                            price=items.price,amount=items.amount,username=username,id=id)
    # print(insertTonnageRizal())
    return  {'Messeges':'Data has been Save'}


#============================================Rizal Tonnage Frame=========================================
from config.models import insertTonnageRizal,getallTonnage,getAllTonnage_checking
from models.model import RizalTonnagehaul
@employee_user.post("/api-insert-rizalTonnage-employeeLogin/")
async def insertTonnage(items: RizalTonnagehaul,username: str = Depends(EmployeevalidateLogin)):
    """This function is to update employee Details"""
    today = datetime.now()
    insertTonnageRizal(transDate=items.transDate,equipment_id=items.equipment_id,
                       tripTicket=items.tripTicket,totalTrip=items.totalTrip, totalTonnage=items.totalTonnage,
                       rate=items.rate,amount=items.amount,driverOperator=items.driverOperator,
                       user=username,date_credited=today)
    # print(insertTonnageRizal())
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
                "amount": "{:.2f}".format(i.amount),
                "totalAmount": "{:,.2f}".format(totalAmount),
                "driverOperator": i.driverOperator,
                "user": i.user,
        })

        rentalData.append(data)

    return rentalData

from config.models import tonnageSumRizal
@employee_user.get("/api-get-rizal-sumTonnage-employeeLogin/")
async def get_SumTonnageRizal(datefrom,dateto,equipment_id:Optional[str],
                            username: str = Depends(EmployeevalidateLogin)):
    """This function is to update employee Details"""
    results = tonnageSumRizal(datefrom=datefrom,dateto=dateto,equipment_id=equipment_id)

    tonnageData = [
        
            {
              
                "equipment_id": i.equipment_id,
                "totalTons": i.totalTons,
                "rate": i.rate,
                "totalAmount":"{:,.2f}".format(float(i.totalTons) * float(i.rate)),
                "totalAmount2": "{:.2f}".format(float(i.totalTons) * float(i.rate))
            
            }
            for i in results
        ]
    

    return tonnageData


@employee_user.get("/api-get-rizal-insertTonnageCheck-employeeLogin/")
async def get_dieselChecker(tripTicket:Optional[str],
                            username: str = Depends(EmployeevalidateLogin)):
    """This function is to update employee Details"""
    results = getAllTonnage_checking(tripTicket=tripTicket)

    DieselData = [
        
            {
              
                "tripTicket": i.tripTicket,
                
            
            }
            for i in results
        ]
    

    return DieselData
#===================================================Inventory Frame =======================================
@employee_user.get("/inventory-frame-rizal/", response_class=HTMLResponse)
async def inventory_frame_rizal(request: Request, username: str = Depends(EmployeevalidateLogin)):
    return templates.TemplateResponse("rizal/inventory.html", {"request":request})


@employee_user.post("/api-insert-inventory-rizal-employee/")
async def insert_inventory(items:InventoryItemsModel, username: str = Depends(EmployeevalidateLogin)): # this is for inserting inventory item
    
    try:
        insert_invetory_item(item_name=items.item_name, description=items.description,
                             category=items.category,uom=items.uom,
                            supplier=items.supplier,price=items.price,quantity_in_stock=items.quantity_in_stock,
                            minimum_stock_level=items.minimum_stock_level,location=items.location, user=username)
        # return('Data has been Save')


    except Exception as ex:
        error_message = f"Error due to: {str(ex)}"
        return {"error": error_message}
    return {"message":"User has been save"} 

#===============================================Cost Frame Function =======================================

from config.models import insertCost,select_cost, getTonnage_id
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



@employee_user.get("/update-tonnage-haul-employeeLogin/{id}", response_class=HTMLResponse)
async def get_updatetonnageHaul(request:Request,id, username: str = Depends(EmployeevalidateLogin)):
    """This function is for dispalying Diesel Transaction using ID"""
    myresult = getTonnage_id(id=id)


    tonnageData = [
        
            {

                "id": x.id,
                "transDate": x.transDate,
                "equipment_id": x.equipment_id,
                "tripTicket": x.tripTicket,
                "totalTrip": x.totalTrip,
                "totalTonnage": x.totalTonnage,
                "rate": x.rate,
                "amount": "{:,.2f}".format(x.amount),
                "driverOperator": x.driverOperator
            

            }
            for x in myresult
        ]

  
   
    
    

    return  templates.TemplateResponse("employee/uptonnage_rizal.html", 
                                        {"request":request,"tonnageData":tonnageData,"user":username
                                        })

@employee_user.put("/api-update-tonnage-haul-employeeLogin/{id}")
async def updateTons_rizal(id,items:RizalTonnagehaul, username: str = Depends(EmployeevalidateLogin)):
    """This function is for updating Tons in Rizal"""
    today = datetime.now()

    updateTonnage(transDate=items.transDate,equipment_id=items.equipment_id,
                    tripTicket=items.tripTicket,totalTrip=items.totalTrip,
                    totalTonnage=items.totalTonnage,rate=items.rate,
                    amount=items.amount,driverOperator=items.driverOperator,user=username,
                    date_updated=today,id=id)

    return {'Message': 'Data has been Updated'}



# this is for inserting employee
from models.model import EmployeeReg2
from config.models import insertEmployee
@employee_user.post("/api-insert-employee-employeeLogin")
async def insertEmployee_empLogin(items:EmployeeReg2, username: str = Depends(EmployeevalidateLogin)):
    insertEmployee(lastName=items.lastName,
                            firstName=items.firstName,
                            middleName=items.middleName,
                            gender=items.gender,
                            address_employee=items.address_employee,
                            contactNumber=items.contactNumber,
                            contact_person=items.contact_person,
                            emer_cont_person=items.emer_cont_person,
                            position=items.position,
                            date_hired=items.date_hired,
                            department=items.department,
                            end_contract=items.end_contract,
                            tin=items.tin,
                            sssNumber=items.sssNumber,
                            phicNumber=items.phicNumber,
                            hdmfNumber=items.hdmfNumber,
                            employment_status=items.employment_status,
                            salary_rate=items.salary_rate,
                            taxCode=items.taxCode,
                            off_on_details=items.off_on_details,
                            Salary_Detail=items.Salary_Detail,
                            employee_id=items.employee_id,user=username)
    return {'Message': 'Data has been Save'}

#======================================TVI Employee Transaction Frame=======================================
from config.tvi_models import (insertRental_tvi,insertRental_tvi_employeeLogin,
                                getRentalTVI_all_employeeLogin,rentalSumTVI,
                                insertDiesel_tvi,deleteRental)

from models.model import TVIRentalTransactionEmployeeLogin,TVIDiesel
@employee_user.get("/employee-transaction-tvi/", response_class=HTMLResponse)
async def api_login(request: Request, username: str = Depends(EmployeevalidateLogin)):
    return templates.TemplateResponse("employee/tvi_employee_trans.html", {"request":request}) 

@employee_user.post("/api-insert-tvi-rental-employeeLogin/")
async def insertRentalTVI(items:TVIRentalTransactionEmployeeLogin,user: str = Depends(EmployeevalidateLogin)):
    """This function is to update employee Details"""
    today = datetime.now()
    insertRental_tvi_employeeLogin(transDate=items.transDate,demr=items.demr,
                            equipmentId=items.equipmentId,time_in=items.time_in,time_out=items.time_out,
                            totalHours=items.totalHours,rentalRate=items.rentalRate,
                            totalAmount=items.totalAmount,taxRate=items.taxRate, vat_output=items.vat_output,
                            net_of_vat=items.net_of_vat,date_credited=today, 
                            project_site=items.project_site,driverOperator=items.driverOperator,user=user)
    return  {'Messeges':'Data has been Save'}                        


@employee_user.get("/api-get-tvi-rental-employeeLogin/")
async def get_cost(datefrom,dateto,equipmentId:Optional[str],
                    project_site:Optional[str],username: str = Depends(EmployeevalidateLogin)):
    """This function is to update employee Details"""
    results = getRentalTVI_all_employeeLogin(datefrom=datefrom,dateto=dateto,
                                                project_site=project_site,equipmentId=equipmentId)

    rentalData = [
        
            {
                "id": x.id,
                "transDate": x.transDate,
                "demr": x.demr,
                "equipmentId": x.equipmentId,
                "time_in": x.time_in,
                "time_out": x.time_out,
                "totalHours": "{:,.2f}".format(x.totalHours),
                "rentalRate": "{:,.2f}".format(x.rentalRate),
                "totalAmount": "{:,.2f}".format(x.totalAmount),
                "taxRate": "{:,.2f}".format(x.taxRate),
                "vat_output": "{:,.2f}".format(x.vat_output),
                "net_of_vat": "{:,.2f}".format(x.net_of_vat),
                "project_site":x.project_site,
                "driverOperator":x.driverOperator,
                "user": x.user,
                "date_updated": x.date_updated,
                "date_credited": x. date_credited
            
            }
            for x in results
        ]
    

    return rentalData


@employee_user.get("/api-get-rentalSum-employeeLogin/")
async def getRentalSum(datefrom,dateto,equipmentId:Optional[str],username: str = Depends(EmployeevalidateLogin)):
    """This function is for testing"""


    data = rentalSumTVI(datefrom=datefrom,dateto=dateto,equipmentId=equipmentId)

    rentalData = []

    for i in data:
       
        # totalAmount+=i.amount
        totalHours = i.totalHours
        rentalRate = i.rentalRate
        totalAmount = float(totalHours) * float(rentalRate)

        data={}   
        
        data.update({
                "equipmentId": i.equipmentId,
                "totalHours": i.totalHours,
                "rentalRate": i.rentalRate,
                "totalAmount":  "{:,.2f}".format(totalAmount)
        })

        rentalData.append(data)

    return rentalData




#=================================================TVI Diesel Transaction Frame===================================
from config.tvi_models import DiesellSumTVI
@employee_user.post("/api-insert-tvi-diesel-employeeLogin/")
async def insertDieselTviEmployeeLogin(items:TVIDiesel,username: str = Depends(EmployeevalidateLogin)):
    """This function is to insert """
    today = datetime.now()
    insertDiesel_tvi(transDate=items.transDate,equipmentId=items.equipmentId,
                        withdrawalSlip=items.withdrawalSlip,totalliters=items.totalliters,
                        price=items.price,totalAmount=items.totalAmount,
                        user=username,date_credited=today)


@employee_user.get("/api-get-tvi-diesel-employeeLogin/")
async def getDieselSum(datefrom,dateto,username: str = Depends(EmployeevalidateLogin)):
    """This function is to update employee Details"""
    results = DiesellSumTVI(datefrom=datefrom,dateto=dateto)

    dieselData = [
        
            {
                "equipmentId": x.equipmentId,
                "totalliters": "{:,.2f}".format(x.totalliters),
                "totalAmount": "{:,.2f}".format(x.totalAmount),
               
            }
            for x in results
        ]
    

    return dieselData


#=============================================Employee Details=========================================
from config.models import getAllEmployee_TVI
@employee_user.get("/api-get-tvi-employeeDetails-employeeLogin/")
async def getDieselSum(username: str = Depends(EmployeevalidateLogin)):
    """This function is to update employee Details"""
    results = getAllEmployee_TVI()

    employeeData = [
        
            {
                "employee_id": x.employee_id,
                "lastName": x.lastName,
                "firstName": x.firstName,
                "position": x.position,
                "department": x.department,
                "off_on_details": x.off_on_details,
                "employment_status": x.employment_status

               
            }
            for x in results
        ]
    
   
    return employeeData

@employee_user.get("/tvi-payroll-transaction/", response_class=HTMLResponse)
async def api_login(request: Request, username: str = Depends(EmployeevalidateLogin)):
    return templates.TemplateResponse("employee/tvi_payroll.html", {"request":request}) 

#==============================================TVI Tons Transaction===================================
from config.tvi_models import (getRoutes,insertRoutes,
                                routesAutocomplete,insertTons,getTon,getTons,
                                getTon_id,updateTons,getIncentives)
from models.model import TVIRoutes,TVITons
@employee_user.get("/api-get-tvi-check-routes-employeeLogin/")
async def getroutesTVI(routes,username: str = Depends(EmployeevalidateLogin)):
    """This function is for checking if routes has been already exist"""

    results = getRoutes(routes=routes)

    routesData = [
        
            {
                "id": x.id,
                "routes": x.routes,
                "distance": x.distance,
                
            }
            for x in results
        ]
    
   
    return routesData


@employee_user.post("/api-insert-tvi-routes-employeeLogin/")
async def insertRoutesEmployeeLogin(items:TVIRoutes,username: str = Depends(EmployeevalidateLogin)):
    """This function is to insert """
    
    insertRoutes(routes=items.routes,distance=items.distance)


@employee_user.get("/api-search-autocomplete-tvi-routes/")
def autocomplete_tvi_routes(term: Optional[str]):
    # this is to autocomplete Routes
    items = routesAutocomplete(term=term)

    
    suggestions = []
    for item in items:
        suggestions.append(item.routes)
 
    return suggestions


@employee_user.get("/api-get-tvi-check-tons-employeeLogin/")
async def getroutesTVI(tripTicket,username: str = Depends(EmployeevalidateLogin)):
    """This function is for checking if routes has been already exist"""

    results = getTon(tripTicket=tripTicket)

    tonData = [
        
            {
                "id": x.id,
                "routes": x.routes,   
            }
            for x in results
        ]
    
   
    return tonData


@employee_user.post("/api-insert-tvi-tons-employeeLogin/")
async def insertTonsEmployeeLogin(items:TVITons,username: str = Depends(EmployeevalidateLogin)):

    """This function is to insert """
    
    insertTons(transDate=items.transDate,equipmentId=items.equipmentId,tripTicket=items.tripTicket,
                routes=items.routes,trips=items.trips,volume_tons=items.volume_tons,
                distance=items.distance,hauling_rate=items.hauling_rate,
                project_site=items.project_site,driverOperator=items.driverOperator,
                user=username)
    

@employee_user.get("/api-get-tvi-tons-employeeLogin/")
async def get_cost(datefrom,dateto,equipmentId:Optional[str],
                    project_site:Optional[str],username: str = Depends(EmployeevalidateLogin)):
    """This function is to update employee Details"""
    results = getTons(datefrom=datefrom,dateto=dateto,
                        project_site=project_site,equipmentId=equipmentId)

    rentalData = [
        
            {
                "id": x.id,
                "transDate": x.transDate,
                "equipmentId": x.equipmentId,
                "tripTicket": x.tripTicket,
                "routes": x.routes,
                "trips": x.trips,
                "volume_tons": x.volume_tons,
                "distance": x.distance,
                "hauling_rate": x.hauling_rate,
                "billingAmount":(float(x.volume_tons) * float(x.distance) * float(x.hauling_rate)),
                "billingAmount2": "{:,.2f}".format(float(x.volume_tons) * float(x.distance) * float(x.hauling_rate)),
                
            
            }
            for x in results
        ]
    

    return rentalData

@employee_user.get("/api-get-update-tvi-tonsTransaction-sqlModel/{id}", response_class=HTMLResponse)
async def getTviTrans(id: int,request:Request,username: str = Depends(EmployeevalidateLogin)):
    """This function is for querying from Rental Transactions for update purposes"""

    x = getTon_id(id=id)

    tonsData = [
        
            {
                "id": x.id,
                "transDate": x.transDate,
                "equipmentId": x.equipmentId,
                "tripTicket": x.tripTicket,
                "routes": x.routes,
                "trips": x.trips,
                "volume_tons": x.volume_tons,
                "distance": x.distance,
                "hauling_rate": x.hauling_rate,
                "billingAmount":(float(x.volume_tons) * float(x.distance) * float(x.hauling_rate)),
                "billingAmount2": "{:,.2f}".format(float(x.volume_tons) * float(x.distance) * float(x.hauling_rate)),
                "driverOperator": x.driverOperator
            
            }
            
        ]
    
    return templates.TemplateResponse("tvi/updatetonsTVI.html",{'request':request,'tonsData':tonsData})


@employee_user.put("/api-update-tvi-tons-sqlModel/{id}")
async def insertRentalTvi(id: int, items:TVITons,username: str = Depends(EmployeevalidateLogin)):
    """This function is to update tons Details"""
    today = datetime.now()
    updateTons(transDate=items.transDate,equipmentId=items.equipmentId,tripTicket=items.tripTicket,
                    routes=items.routes,trips=items.trips,volume_tons=items.volume_tons,
                    distance=items.distance,hauling_rate=items.hauling_rate,project_site=items.project_site,
                    driverOperator=items.driverOperator,user=username,date_updated=today,id=id)


    return  {'Messeges':'Data has been Save'}  


@employee_user.get("/api-get-tvi-tons-incentives/")
async def get_cost(datefrom,dateto,equipmentId: Optional[str],username: str = Depends(EmployeevalidateLogin)):
    """This function is to update employee Details"""
    results = getIncentives(datefrom=datefrom,dateto=dateto,equipmentId=equipmentId)

    tonsData = [
        
            {
                
                "equipmentId": x.equipmentId,
                "routes": x.routes,
                "trips": x.trips,
                "distance": x.distance,
                "driverOperator": x.driverOperator,
                "incentives": "{:.2f}".format(float(x.trips) * float(x.distance) * 25)
            }
            for x in results
        ]
    
    
    return tonsData

#==================================================API TVI Payroll=======================================================
from models.model import TVIPayroll
from config.tvi_models import insertPayroll,getPayrollTvi
@employee_user.post("/api-insert-tvi-payroll/")
async def insertPayroll_TVI(items:TVIPayroll, username: str = Depends(EmployeevalidateLogin)):
    """This function is for inserting payroll TVI adan"""
    insertPayroll(transDate=items.transDate,employee_id=items.employee_id,first_name=items.first_name,
                    last_name=items.last_name,salaryRate=items.salaryRate,addOnRate=items.addOnRate,
                        salaryDetails=items.salaryDetails,regDay=items.regDay,regDayOt=items.regDayOt,
                        sunday=items.sunday,sundayOT=items.sundayOT,spl=items.spl,
                        splOT=items.splOT,lgl2=items.lgl2,lgl2OT=items.lgl2OT,nightDiff=items.nightDiff,
                        adjustment=items.adjustment,lgl1=items.lgl1, user=username)

@employee_user.get("/api-get-tvi-payroll/")
async def get_cost(datefrom:Optional[date],dateto: Optional[date],username: str = Depends(EmployeevalidateLogin)):
    """This function is to update employee Details"""
    results = getPayrollTvi(datefrom=datefrom,dateto=dateto)

    payrollData = [
        
            {
                
                "transDate": x.transDate,
                "employee_id": x.employee_id,
                "first_name": x.first_name,
                "last_name": x.last_name,
                "salaryRate": x.salaryRate,
                "addOnRate": x.addOnRate,
                "regDay": x.regDay,
                "regDayCal": "{:.2f}".format(float(x.addOnRate) * float(x.regDay)),
                "regDayOt": x.regDayOt,
                "regDayOtCal": "{:.2f}".format(float(x.salaryRate)/8 * 1.25 * float(x.regDayOt)),
                "sunday": x.sunday,
                "sundayCal": "{:.2f}".format(float(x.salaryRate) * (1.30) * float(x.sunday)),
                "sundayOT": x.sundayOT,
                "sundayOTCal": "{:.2f}".format(float(x.salaryRate) / 8 * (1.69) * float(x.sundayOT)),
                "spl": x.spl,
                "splCal": "{:.2f}".format(float(x.salaryRate) * (1.30) * float(x.spl)),
                "splOT": x.splOT,
                "splOTCal": "{:.2f}".format(float(x.salaryRate) / 8 * (1.69) * float(x.splOT)),
                "lgl2": x.lgl2,
                "lgl2Cal": "{:.2f}".format(float(x.salaryRate) * (2) * float(x.lgl2)),
                "lgl2OT": x.lgl2OT,
                "lgl2OTCal": "{:.2f}".format(float(x.salaryRate) / 8 * (2) * (1.30) * float(x.lgl2OT)),
                "lgl1": x.lgl1,
                "lgl1Cal": "{:.2f}".format(float(x.salaryRate) * float(x.lgl1)),
                "nightDiff": x.nightDiff,
                "nightDiffCal": "{:.2f}".format(float(x.nightDiff)),
                "adjustment": x.adjustment


                # "nightDiffCal": "{:.2f}".format(float(x.salaryRate)/8 * 0.10 * float(x.nightDiff)),
                
                #"regDayCal": "{:.2f}".format((float(x.salaryRate) + (float(x.salaryRate) * .1675213)) * float(x.regDay))
                # "regDayCal": "{:.2f}".format(float(x.salaryRate) + (float(x.salaryRate) * .1675213)) * float(x.regDay)
                #"{:.2f}".format(float(x.addOnRate) * float(x.regDay))
                # "incentives": "{:.2f}".format(float(x.trips) * float(x.distance) * 25)
            }
            for x in results
        ]
    
    
    return payrollData


@employee_user.get("/tvi-diesel-update-employeeLogin/", response_class=HTMLResponse)
async def api_login(request: Request, username: str = Depends(EmployeevalidateLogin)): # this is for GRC transaction
    return templates.TemplateResponse("employee/updateDieselTvi.html", {"request":request})
from models.model import TviDiesel
from config.tvi_models import getDieselTVI_all, updateTVIDiesel
@employee_user.get("/api-search-autocomplete-tiv-diesel-transaction/")
def autocomplete_grc_equipment(term: Optional[int] = None,username: str = Depends(EmployeevalidateLogin)):
   
    # Ensure you're correctly handling query parameters, 'term' in this case

    dieselData = getDieselTVI_all()

    if term:
       filtered_equipment = [item for item in dieselData if term == item.id]
    else:
        filtered_equipment = []

    suggestions = [{"value": item.id,
                    "transDate": item.transDate,
                    "equipmentId": item.equipmentId,
                    "withdrawalSlip": item.withdrawalSlip,
                    "totalliters": item.totalliters,
                    "price": item.price,
                    "totalAmount": item.totalAmount,
                    
                    } for item in filtered_equipment]
    return suggestions


@employee_user.put("/api-update-tiv-diesel-employeeLogin/")
async def updateDieselTviEmployeeLogin(id: int,items: TviDiesel,username: str = Depends(EmployeevalidateLogin)):
    """This function is to update employee Details"""
    today = datetime.now()
    updateTVIDiesel(transDate=items.transDate,equipmentId=items.equipmentId,withdrawalSlip=items.withdrawalSlip,
                        totalliters=items.totalliters,price=items.price,
                        totalAmount=items.totalAmount,user=username,date_updated=today,id=id)
                        
    # print(insertTonnageRizal())
    return  {'Messeges':'Data has been Save'}

# ============================================GRC Transaction ============================================

from config.grcDB import GrcViews
@employee_user.get("/grc-payroll-transaction/", response_class=HTMLResponse)
async def api_login(request: Request, username: str = Depends(EmployeevalidateLogin)): # this is for GRC transaction
    return templates.TemplateResponse("employee/grc_payroll.html", {"request":request})


@employee_user.post("/api-insert-grc-payroll/")
async def insertPayroll_GRC(items:TVIPayroll, username: str = Depends(EmployeevalidateLogin)):
    """This function is for inserting payroll  adan"""
    GrcViews.insertGrcPayrollAdan(transDate=items.transDate,employee_id=items.employee_id,first_name=items.first_name,
                    last_name=items.last_name,salaryRate=items.salaryRate,addOnRate=items.addOnRate,
                        salaryDetails=items.salaryDetails,regDay=items.regDay,regDayOt=items.regDayOt,
                        sunday=items.sunday,sundayOT=items.sundayOT,spl=items.spl,
                        splOT=items.splOT,lgl2=items.lgl2,lgl2OT=items.lgl2OT,nightDiff=items.nightDiff,
                        adjustment=items.adjustment,lgl1=items.lgl1, user=username)

    return('Data has been Save')




