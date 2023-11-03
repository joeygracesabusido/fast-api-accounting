from fastapi import APIRouter, Body, HTTPException, Depends, Request, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Union, List, Optional
from datetime import datetime, date

from schemas.user import usersEntity

from models.model import SgmcEquipment, RentalSgmc
from config.sgmcDB import SGMCViews

# from config.db import mydb
# from config.db import create_mongo_client
# mydb = create_mongo_client()

from config.mongodb_con import create_mongo_client
mydb = create_mongo_client()

from jose import jwt

JWT_SECRET = 'myjwtsecret'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

sgmcRouter = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")

from authentication.utils import OAuth2PasswordBearerWithCookie
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


from config.grcDB import GrcViews

oauth_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")


def ValidationLogin(request:Request):
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


@sgmcRouter.get("/employee-transaction-sgmc/", response_class=HTMLResponse)
async def sgmc_template(request: Request, username: str = Depends(ValidationLogin)):
    return templates.TemplateResponse("sgmc/sgmc_transaction.html", {"request":request}) 

@sgmcRouter.post("/insert-equipment-sgmc/")
async def insert_rental_sgmc(items:SgmcEquipment, username: str = Depends(ValidationLogin)):
    """This function is for inserting equipment to GRC table"""
    try:
        SGMCViews.insert_equipment_sgmc(equipment_id=items.equipment_id,equipmentDiscription=items.equipmentDiscription,
                                        rentalRate=items.rentalRate, comments=items.comments,owners=items.owners,
                                        user=username,date_credited=datetime.now())

        return('Data has been Save')

    except Exception as e:
        error_message = str(e)  # Use the actual error message from the exception
       
        return {"error": error_message}

@sgmcRouter.get("/api-search-autocomplete-sgmc-equipment/")
def autocomplete_grc_equipment(term: Optional[str] = None): # this is for autocomplete of equipment

    # Ensure you're correctly handling query parameters, 'term' in this case

    equipment = SGMCViews.getEquipment()

    if term:
        filtered_equipment = [item for item in equipment if term.lower() in item.equipment_id.lower()]
    else:
        filtered_equipment = []

    suggestions = [{"value": item.equipment_id,"rentalRate": item.rentalRate} for item in filtered_equipment]
    return suggestions

@sgmcRouter.post("/api-insert-grc-rental/")
async def insert_rental_GRC(items:RentalSgmc, username: str = Depends(ValidationLogin)):
    """This function is for inserting equipment to GRC table"""
    try:
        SGMCViews.insert_rental_sgmc(transDate=items.transDate,demr=items.demr,equipment_id=items.equipment_id,
                                    timeIn=items.timeIn,timeOut=items.timeOut,totalHours=items.totalHours,
                                        rentalRate=items.rentalRate,amount=items.amount,
                                            shift=items.shift,driver_operator=items.driver_operator,user=username,
                                            date_credited=datetime.now)

        return('Data has been Save')

    except Exception as e:
        error_message = str(e)  # Use the actual error message from the exception
       
        return {"error": error_message}