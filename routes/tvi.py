from traceback import format_list
from fastapi import APIRouter, Body, HTTPException, Depends, Request, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Dict
from config.db import mydb


from bson import ObjectId
from typing import Optional

from datetime import timedelta, datetime


from jose import jwt

JWT_SECRET = 'myjwtsecret'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

tviProject = APIRouter(include_in_schema=False)


templates = Jinja2Templates(directory="templates")


#==================================================This is for user validation====================================
from schemas.user import usersEntity
def validateLogin(request:Request):

    try :
        token = request.cookies.get('access_token')
        if token is None:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Not Authorized",
           
            )
        else:
            scheme, _, param = token.partition(" ")
            payload = jwt.decode(param, JWT_SECRET, algorithms=ALGORITHM)
        
            username = payload.get("sub")
            user =  usersEntity(mydb.login.find({"username":username}))
            

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
            detail= "Not Authorized please Login",
            # headers={"WWW-Authenticate": "Basic"},
        )

from config.tviDB import TviDB
TviDB.initialize() # this is to inialized database of TVI



@tviProject.get("/tvi-transaction/", response_class=HTMLResponse)
async def getTviTrans(request:Request,username: str = Depends(validateLogin)):
    """This function is for querying income statement"""
    return templates.TemplateResponse("tvi/tviEquipment.html",{'request':request})


#==========================================Equipment Frame==================================================
from models.model import tviEquipment
@tviProject.post('/api-insert-tvi-equipment/')
def insertTviEquipment(
    item: tviEquipment, username: str = Depends(validateLogin)):
    #-> Dict[str, str]
    """This function is for inserting Data of Equipment"""

    try:
        # Insert the equipment into the database
        TviDB.insertEquipment(
            equipmentID=item.equipmentId,
            equipmentDesc=item.equipmentDesc,
            rentalRate=item.rentalRate,
            remarks=item.remarks,
        )
    except Exception as ex:
        # Return an error message if an exception is thrown
        return {"Error": f"Error occurred: {str(ex)}"}

    # Return a success message if the operation was successful
    return {"Message": "Data has been saved"}


@ tviProject.get('/api-get-tvi-equipment/')
def get_equipment(username: str = Depends(validateLogin)):
    """This function is for querying all Equipment"""
    equipmentList = TviDB.selectAllEquipment()

    equipmentData = [
            {
                "id": x[0],
                "equipmentID": x[1],
                "equipmentDesc": x[2],
                "rentalRate": x[3],
                "remarks": x[4],
            }
            for x in equipmentList
        ]
       
    return equipmentData

@ tviProject.get('/api-get-tvi-equipment-id/')
def getEquipmentID(id,username: str = Depends(validateLogin)):
    """This function is for querying all Equipment"""
    equipmentList = TviDB.selectEquipment(id=id)

    equipmentData = [
            {
                "id": x[0],
                "equipmentID": x[1],
                "equipmentDesc": x[2],
                "rentalRate": x[3],
                "remarks": x[4],
            }
            for x in equipmentList
        ]
       
    return equipmentData


@tviProject.put('/api-update-tvi-equipment/{id}')
def update_equipment(id,item:tviEquipment,username: str = Depends(validateLogin)):
    """This function is to update equipment """
    TviDB.update_equipment(equipmentId=item.equipmentId,
                            equipmentDesc=item.equipmentDesc,
                            rentalRate=item.rentalRate,
                            remarks=item.remarks,id=id)
    return  {'Messeges':'Data has been updated'}

from models.model import tviRentalTrans
@tviProject.post('/api-insert-tvi-rental-transaction/')
def insertRental(
    item: tviRentalTrans, username: str = Depends(validateLogin)):
    #-> Dict[str, str]
    """This function is for inserting Data of Rental Transaction DB"""

    try:
        # Insert the equipment into the database
        TviDB.insertRental(
            transDate=item.transDate,
            equipmentId=item.equipmentId,
            totalHours=item.totalHours,
            rentalRate=item.rentalRate, 
            taxRate=item.taxRate,
            vat_output=item.vat_output,
            driverOperator=item.driverOperator,
            user=item.user,
            date_credited=item.date_credited
        )
    except Exception as ex:
        # Return an error message if an exception is thrown
        return {"Error": f"Error occurred: {str(ex)}"}

    # Return a success message if the operation was successful
    return {"Message": "Data has been saved"}



