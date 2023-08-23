from fastapi import APIRouter, Body, HTTPException, Depends, Request, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Union, List, Optional
from datetime import datetime, date

from schemas.user import usersEntity


from config.db import mydb


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

from models.model import EquipmentGRC,GrcRentalModels
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

    suggestions = [{"value": item.equipment_id,"rentalRate": item.rentalRate} for item in filtered_equipment]
    return suggestions


@grcRouter.get("/api-search-autocomplete-grc-employee/")
def autocomplete_grc_employee(term: Optional[str] = None):
    # this is to autocomplete Routes
    # Ensure you're correctly handling query parameters, 'term' in this case

    employeeData = getAllEmployee_Surigao()
    

    if term:
        filtered_employee = [item for item in employeeData if term.lower() in item.lastName.lower()  or term.lower() in item.firstName.lower() ]
       
    else:
        filtered_employee = []

    suggestions = [{"value": item.lastName + " , " + item.firstName} for item in filtered_employee]
    print(suggestions)
    return suggestions
   
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