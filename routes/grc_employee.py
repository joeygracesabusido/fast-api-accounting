from fastapi import APIRouter, Body, HTTPException, Depends, Request, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Union, List, Optional
from datetime import datetime, date

from schemas.user import usersEntity

# from config.db import mydb
# from config.db import create_mongo_client
# mydb = create_mongo_client()

from config.mongodb_con import create_mongo_client
mydb = create_mongo_client()

from jose import jwt

JWT_SECRET = 'myjwtsecret'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

grcRouter = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")

from authentication.utils import OAuth2PasswordBearerWithCookie
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


from config.grcDB import GrcViews

oauth_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")


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

@grcRouter.get("/employee-transaction-grc/", response_class=HTMLResponse)
async def grc_template(request: Request, username: str = Depends(EmployeevalidateLogin)):
    return templates.TemplateResponse("employee/grc_employee_trans.html", {"request":request}) 


@grcRouter.get('/grc-payroll-list-employeeLogin/')
async def payrollList(datefrom: Optional[date] = None,
                        dateto: Optional[date] = None,
                        employeeID: Optional[str] = None,
                        username: str = Depends(EmployeevalidateLogin)):
    """This is to get Payroll Transaction from GRC table"""

    results = GrcViews.getPayroll(datefrom=datefrom,dateto=dateto,employeeID=employeeID)

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


              
            }
            for x in results
        ]
    
    
    return payrollData


@grcRouter.get('/grc-13month-list-grc/')
async def payrollList(datefrom: Optional[date] = None,
                        dateto: Optional[date] = None,
                        employeeID: Optional[str] = None,
                        username: str = Depends(EmployeevalidateLogin)):
    """This is to get Payroll Transaction from GRC table"""

    results = GrcViews.get_13_month(datefrom=datefrom,dateto=dateto,employeeID=employeeID)

    payrollData = [
        
            {
            
                "employee_id": x.employee_id,
                "first_name": x.first_name,
                "last_name": x.last_name,
                "salaryRate": x.salaryRate,
                "regDay": x.regDay,
                "sunday": x.sunday,
                "spl": x.spl,
                "lgl2": x.lgl2,
                "lgl1": x.lgl1,
                "total_amount": float(x.regday) * float(x.salary_rate)
              
            }
            for x in results
        ]
    
    
    return payrollData




from config.models import getAllEmployee_Surigao
@grcRouter.get("/api-get-grc-employeeDetails-employeeLogin/")
async def getEmployeeSurigao(username: str = Depends(EmployeevalidateLogin))->List:
    """This function is to update employee Details"""
    results = getAllEmployee_Surigao()

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

from models.model import EquipmentGRC,GrcRentalModels,GrcDiesel,CostSGMC_model
from config.grcDB import GrcViews
@grcRouter.post("/api-insert-grc-equipment/")
async def insertPayroll_GRC(items:EquipmentGRC, username: str = Depends(EmployeevalidateLogin)):
    """This function is for inserting equipment to GRC table"""
    GrcViews.insertEquipmentGRC(equipment_id=items.equipment_id,equipmentDiscription=items.equipmentDiscription,
                                    rentalRate=items.rentalRate,comments=items.comments,
                                    owners=items.owners,user=username)

    return('Data has been Save')


@grcRouter.get("/api-search-autocomplete-grc-equipment/")
def autocomplete_grc_equipment(term: Optional[str] = None):
    # this is to autocomplete Routes

    
    # Ensure you're correctly handling query parameters, 'term' in this case

    equipment = GrcViews.getEquipment()

    if term:
        filtered_equipment = [item for item in equipment if term.lower() in item.equipment_id.lower()]
    else:
        filtered_equipment = []

    suggestions = [{"value": item.equipment_id,"rentalRate": item.rentalRate,"id": item.id} for item in filtered_equipment]
    return suggestions


@grcRouter.get("/api-search-autocomplete-grc-employee/")
def autocomplete_grc_employee(term: Optional[str] = None):
    # this is to autocomplete Routes
    # Ensure you're correctly handling query parameters, 'term' in this case
    try:

        employeeData = getAllEmployee_Surigao()
        

        if term:
            filtered_employee = [item for item in employeeData if term.lower() in item.lastName.lower()  or term.lower() in item.firstName.lower() ]
        
        else:
            filtered_employee = []

        suggestions = [{"value": item.lastName + " , " + item.firstName} for item in filtered_employee]
       
        return suggestions

    except Exception as e:
        error_message = str(e)  # Use the actual error message from the exception
        
        return {"error": error_message}
   
@grcRouter.post("/api-insert-grc-rental/")
async def insert_rental_GRC(items:GrcRentalModels, username: str = Depends(EmployeevalidateLogin)):
    """This function is for inserting equipment to GRC table"""
    try:
        GrcViews.insertRentalGRC(transDate=items.transDate,demr=items.demr,equipment_id=items.equipment_id,
                                    timeIn=items.timeIn,timeOut=items.timeOut,totalHours=items.totalHours,
                                        rentalRate=items.rentalRate,amount=items.amount,
                                            shift=items.shift,driver_operator=items.driver_operator,user=username)

        return('Data has been Save')

    except Exception as e:
        error_message = str(e)  # Use the actual error message from the exception
       
        return {"error": error_message}


@grcRouter.get("/api-get-grc-rental-transaction-employeeLogin/")
async def getRental_views(datefrom: Optional[date],dateto:Optional[date],equipment_id: Optional[str],
                            username: str = Depends(EmployeevalidateLogin))->List:
    """This function is to update employee Details"""
    results = GrcViews.getRental(datefrom=datefrom,dateto=dateto,equipment_id=equipment_id)

    rentalData = [
        
            {
               "id": x. id,
                "transDate": x.transDate,
                "demr": x.demr,
                "equipment_id": x.equipment_id,
                "timeIn": x.timeIn,
                "timeOut": x.timeOut,
                "totalHours": x.totalHours,
                "rentalRate": x.rentalRate,
                "amount": x.amount,
                "shift": x.shift,
                "driver_operator": x.driver_operator,
                "user": x.user,

               
            }
            for x in results
        ]
    
   
    return rentalData


@grcRouter.get("/api-get-grc-rentals-transaction-employeeLogin/") # this is to get all rentals
async def getRental_views(username: str = Depends(EmployeevalidateLogin)):
    """This function is to update employee Details"""
    results = GrcViews.getRentals()

    rentalData = [
        
            {
               "id": x. id,
                "transDate": x.transDate,
                "demr": x.demr,
                "equipment_id": x.equipment_id,
                "timeIn": x.timeIn,
                "timeOut": x.timeOut,
                "totalHours": x.totalHours,
                "rentalRate": x.rentalRate,
                "amount": x.amount,
                "shift": x.shift,
                "driver_operator": x.driver_operator,
                "user": x.user,

               
            }
            for x in results
        ]
    
   
    return rentalData

@grcRouter.get("/update-rental-grc/{id}", response_class=HTMLResponse)
async def grc_template(id:Optional[int],request: Request, username: str = Depends(EmployeevalidateLogin)):

    results = GrcViews.getRental_id(item_id=id)

    rentalData = [
        
            {
               "id": results.id,
                "transDate": results.transDate,
                "demr": results.demr,
                "equipment_id": results.equipment_id,
                "timeIn": results.timeIn,
                "timeOut": results.timeOut,
                "totalHours": results.totalHours,
                "rentalRate": results.rentalRate,
                "amount": results.amount,
                "shift": results.shift,
                "driver_operator": results.driver_operator,
                "user": results.user,

               
            }
           
        ]
    
   
    return templates.TemplateResponse("employee/grc_updateRental.html", {"request":request,"rentalData":rentalData})

@grcRouter.put("/api-update-rental-grc-employeeLogin/{id}")
async def updateGRCRental(id,items:GrcRentalModels,username: str = Depends(EmployeevalidateLogin)):
    """This function is to update Rental"""
    today = datetime.now()
    try:
        GrcViews.updateRental(transDate=items.transDate,demr=items.demr,equipment_id=items.equipment_id,
                                timeIn=items.timeIn,timeOut=items.timeOut,
                                totalHours=items.totalHours,rentalRate=items.rentalRate,
                                amount=items.amount,shift=items.shift,driver_operator=items.driver_operator,
                                user=username,date_updated=today,item_id=id)

    except Exception as e:
        error_message = str(e)  # Use the actual error message from the exception
    
        return {"error": error_message}


    return  {'Messeges':'Data has been Updated'}


# ========================================This is for Diesel Transactions====================================
@grcRouter.post("/api-insert-grc-diesel/")
async def insert_diesel_GRC(items:GrcDiesel, username: str = Depends(EmployeevalidateLogin)):
    """This function is for inserting equipment to GRC table"""
    try:
        GrcViews.insertDieselGrc(transDate=items.transDate,withdrawal_slip=items.withdrawal_slip,
                                    equipment_id=items.equipment_id,literUse=items.literUse,
                                    price=items.price,amount=items.amount,user=username)

        return('Data has been Save')

    except Exception as e:
        error_message = str(e)  # Use the actual error message from the exception
       
        return {"error": error_message}


@grcRouter.get("/api-get-grc-diesel-transaction-employeeLogin/")
async def getDiesel_views(datefrom: Optional[date],dateto:Optional[date],equipment_id: Optional[str],
                            username: str = Depends(EmployeevalidateLogin))->List:
    """This function is to update employee Details"""
    results = GrcViews.getDiesel(datefrom=datefrom,dateto=dateto,equipment_id=equipment_id)

    dieselData = [
        
            {
               "id": x. id,
                "transDate": x.transDate,
                "withdrawal_slip": x.withdrawal_slip,
                "equipment_id": x.equipment_id,
                "literUse": x.literUse,
                "price": x.price,
                "amount": x.amount,
                "user": x.user,

               
            }
            for x in results
        ]
    
   
    return dieselData


@grcRouter.get("/update-diesel-grc/{id}", response_class=HTMLResponse)
async def grc_template(id:Optional[int],request: Request, username: str = Depends(EmployeevalidateLogin)):

    results = GrcViews.getDiesel_id(item_id=id)

    dieselData = [
        
            {
              "id": results. id,
                "transDate": results.transDate,
                "withdrawal_slip": results.withdrawal_slip,
                "equipment_id": results.equipment_id,
                "literUse": results.literUse,
                "price": results.price,
                "amount": results.amount,
                "user": results.user,

               
            }
           
        ]
    
   
    return templates.TemplateResponse("employee/grc_updateDiesel.html", {"request":request,"dieselData":dieselData})

@grcRouter.put("/api-update-diesel-grc-employeeLogin/{id}")
async def updateGRCDiesel(id,items:GrcDiesel,username: str = Depends(EmployeevalidateLogin)):
    """This function is to update Rental"""
    today = datetime.now()
    try:
        GrcViews.updateDiesel(transDate=items.transDate,withdrawal_slip=items.withdrawal_slip,
                                    equipment_id=items.equipment_id,literUse=items.literUse,
                                    price=items.price,amount=items.amount,
                                    user=username,date_updated=today,item_id=id)

    except Exception as e:
        error_message = str(e)  # Use the actual error message from the exception
    
        return {"error": error_message}


    return  {'Messeges':'Data has been Updated'}



    # ======================================= Cost Frame ============================================

@grcRouter.post("/api-insert-cost-grc/")
async def insert_cost_sgmc(items:CostSGMC_model, username: str = Depends(EmployeevalidateLogin) ): # this function is for inserting diesel 
    user =  mydb.access_setting.find({"username":username})
    for i in user:
        if i['site'] == 'admin' or i['site'] == 'grc' and i['site_transaction_write']:
            try:
                GrcViews.insert_cost_grc(transDate=items.transDate,equipment_id=items.equipment_id,
                                             cost_details=items.cost_details,amount=items.amount,
                                             particular=items.particular,user=username,
                                             date_created=items.date_created)

                return('Data has been Save')

            except Exception as e:
                error_message = str(e)  # Use the actual error message from the exception
            
                return {"error": error_message}
            
    # error message if not autorized for this transaction
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Not Authorized",
            
            )


@grcRouter.get("/api-get-grc-cost-transaction/")
async def get_update_diesel_views(datefrom: Optional[date],dateto:Optional[date],equipment_id: Optional[str],
                            username: str = Depends(EmployeevalidateLogin))->List:
    """This function is to update employee Details"""
    user =  mydb.access_setting.find({"username":username})
    for i in user:
        if i['site'] == 'admin' or i['site'] == 'sgmc' and i['site_transaction_read']:

            results = GrcViews.get_cost(datefrom=datefrom,dateto=dateto,equipment_id=equipment_id)

            costData_grc = [
                
                    {
                    "id": cost_data. id,
                        "transDate": cost_data.transDate,
                        "equipment_id": equipment_data.equipment_id,
                        "cost_details": cost_data.cost_details,
                        "amount": cost_data.amount,
                        "particular":cost_data.particular,
                        "user": cost_data.user,
                        "date_created": cost_data.date_created,
                       

                    
                    }
                    for cost_data,equipment_data in results
                ]
            
        
            # return dieselData

            # Calculate running total of totalHours
            total_amount = sum(entry['amount'] for entry in costData_grc)
            total_amount2 = '{:,.2f}'.format(total_amount)

            return {"costData_grc": costData_grc, "totalAmount": total_amount2}
        # error message if not autorized for this transaction
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= "Not Authorized",
               
                )



@grcRouter.get("/update-cost-grc/{id}", response_class=HTMLResponse)
async def grc_update_diesel_api(id:Optional[int],request: Request, username: str = Depends(EmployeevalidateLogin)):
    user =  mydb.access_setting.find({"username":username})
    for i in user:
        if i['site'] == 'admin' or i['site'] == 'grc' and i['site_transaction_write']:

            results = GrcViews.getcost_id(item_id=id)
            print(results)
            costData = [
                
                    {
                        "id": cost_data. id,
                        "transDate": cost_data.transDate,
                        "equipment_id": equipment_data.equipment_id,
                        "cost_details": cost_data.cost_details,
                        "amount": cost_data.amount,
                        "particular":cost_data.particular,
                        "user": cost_data.user,
                        "date_created": cost_data.date_created,
                        "equipment_id_id": equipment_data.id,
                    
                    }
                    for cost_data,equipment_data in results
            ]
            
            print(costData)
        
            return templates.TemplateResponse("employee/grc_update_cost.html", {"request":request,"costData":costData})

        # error message if not autorized for this transaction
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= "Not Authorized",
               
                )   

    
@grcRouter.put("/api-update-cost-grc/{id}") # this is to update cost
async def update_cost_sgmc(id,items:CostSGMC_model,username: str = Depends(EmployeevalidateLogin)):
    """This function is to update Rental"""
    today = datetime.now()
    try:
        GrcViews.updateCost(transDate=items.transDate,equipment_id=items.equipment_id,
                                cost_details=items.cost_details,amount=items.amount,
                                particular=items.particular,user=username,
                                date_updated=datetime.now(),item_id=id)
    except Exception as e:
        error_message = str(e)  # Use the actual error message from the exception
    
        return {"error": error_message}


    return  {'Messeges':'Data has been Updated'}  

