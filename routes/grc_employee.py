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