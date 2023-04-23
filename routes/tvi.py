from traceback import format_list
from fastapi import APIRouter, Body, HTTPException, Depends, Request, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Dict
from config.db import mydb


from bson import ObjectId
from typing import Optional

from datetime import timedelta, datetime, date


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
                "owner": x[5],
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
                "owner": x[5],
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
                            remarks=item.remarks,
                            owner=item.owner,id=id)
    return  {'Messeges':'Data has been updated'}


@tviProject.get("/api-search-autocomplete-tvi-equipment/")
def autocomplete_equipmentID(term: Optional[str]):
    items = TviDB.selectEquipmentIDAutocomplete(equipmentId=term)

    suggestions = []
    for item in items:
        suggestions.append(item[1])
        
    return suggestions

#===================================================Rental Transaction=====================================
from models.model import tviRentalTrans,TVIRentalTransaction,TVIDiesel

@ tviProject.get('/api-get-tvi-equipment-equipmentID/')
def getEquipmentID(equipmentID,username: str = Depends(validateLogin)):
    """This function is for querying all Equipment"""
    equipmentList = TviDB.selectEquipmentID(equipmentId=equipmentID)

    equipmentData = [
            {
                "id": x[0],
                "equipmentID": x[1],
                "equipmentDesc": x[2],
                "rentalRate": x[3],
                "remarks": x[4],
                "owner": x[5],
            }
            for x in equipmentList
        ]
       
    return equipmentData




@tviProject.post('/api-insert-tvi-rental-transaction/')
def insertRental(
    item: tviRentalTrans, username: str = Depends(validateLogin)):
    #-> Dict[str, str]
    """This function is for inserting Data of Rental Transaction DB"""
    today = datetime.now()

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
            user=username,
            owner=item.owner,
            date_credited=today
        )
       
    except Exception as ex:
        # Return an error message if an exception is thrown
        return {"Error": f"Error occurred: {str(ex)}"}

    # Return a success message if the operation was successful
    return {"Message": "Data has been saved"}


@ tviProject.get('/api-get-tvi-rental-transactions/')
def get_equipment(datefrom,dateto,equipmentID,owner,username: str = Depends(validateLogin)):
    """This function is for querying all Equipment"""
    rentalList = TviDB.selectAllRental(datefrom=datefrom,dateto=dateto,
                                        equipmentID=equipmentID,onwer=owner)

    rentalData = [
            {
                "id": x[0],
                "transDate": x[1],
                "equipmentID": x[2],
                "totalHours": x[3],
                "rentalRate": x[4],
                "totalAmount": x[5],
                "net_of_vat": x[8],
                "driverOperator": x[9],
                "owner": x[10],
            }
            for x in rentalList
        ]
       
    return rentalData

# @tviProject.delete('/api-deletetiv-rental/{id}')
# def delete_hauling(id,username: str = Depends(validateLogin)):
#     """This function is to delete rental Transaction"""
#     TviDB.delete_rental_trans(id=id)
#     return  {'Messeges':'Data has been deleted'}
@tviProject.delete('/api-deletetiv-rental/{id}')
def delete_rental_transaction(id: int, username: str = Depends(validateLogin)):
    """This function is to delete a rental transaction"""
    try:
        TviDB.delete_rental_trans(id=id)
    except HTTPException as ex:
        return {'message': ex.detail}
    
from config.tvi_models import deleteRental
@tviProject.delete('/api-deletetiv-rental-employeeLogin/{id}')
async def delete_rental_transaction(id: int, username: str = Depends(validateLogin)):
    """This function is to delete a rental transaction"""
    try:
        deleteRental(id=id)
    except HTTPException as ex:
        return {'message': ex.detail}


@tviProject.get('/api-update-tiv-rental-withID/{id}',response_class=HTMLResponse)
async def update_journalEntry_sur(id,request:Request, username: str = Depends(validateLogin)):
    """This function is for updating Journal Entry"""
    rentalList = TviDB.selectRentalperID(id=id)

    rentalData = [
            {
                "id": x[0],
                "transDate": x[1],
                "equipmentID": x[2],
                "totalHours": x[3],
                "rentalRate": x[4],
                "totalAmount": x[5],
                "taxRate": x[6],
                "vat_output": x[7],
                "net_of_vat": x[8],
                "driverOperator": x[9],
                "owner": x[10],
            }
            for x in rentalList
        ]
       
    

    return templates.TemplateResponse('tvi/tviRentalUpdate.html',{'request':request,
                                        'rentalData':rentalData})



@tviProject.put('/api-update-tiv-rental-withID/{id}')
def updateRentalTransaction(id,item:tviRentalTrans,username: str = Depends(validateLogin)):
    """This function is to update equipment """
    today = datetime.today()
    TviDB.update_rentalTrans(transDate=item.transDate,equipmentId=item.equipmentId,
                            totalHours=item.totalHours,rentalRate=item.rentalRate,
                            taxRate=item.taxRate,vat_output=item.vat_output,
                            driverOperator=item.driverOperator,user=username,owner=item.owner,
                            date_updated=today,id=id)
    return  {'Messeges':'Data has been updated'}

 
#=============================================== Equipment Frame SqlModel=================================
from config.tvi_models import equipment_details_tvi, rentaltransaction
from config.tvi_models import (insertEquipment_tvi,select_tivEquipment_id,
                                getEquipmentTVI,select_tivEquipment_with_id,
                                updateTVIequipment,getEquipmentTVI2,insertRental_tvi,getRentalTVI,
                                getRentalTVI_id,getRentalTVI_all,getRentalTVI_id_update,
                                updateTVIrental,insertDiesel_tvi)
@tviProject.post("/api-insert-tvi-equipment-sqlModel/")
async def insertCostapi(items:equipment_details_tvi,username: str = Depends(validateLogin)):
    """This function is to update employee Details"""
    insertEquipment_tvi(equipmentID=items.equipmentID,purchase_date=items.purchase_date,
                    equipmentDesc=items.equipmentDesc,purchase_amount=items.purchase_amount,
                    rentalRate=items.rentalRate,plate_number=items.plate_number,
                    status=items.status,project_site=items.project_site,remarks=items.remarks,owner=items.owner)


    return  {'Messeges':'Data has been Save'}   

@ tviProject.get('/api-get-tvi-equipment-sqlModel/')
def get_equipment(username: str = Depends(validateLogin)):
    """This function is for querying all Equipment"""
    equipmentList = getEquipmentTVI()

    equipmentData = [
            {
                "id": x.id,
                "equipmentID": x.equipmentID,
                "purchase_date": x.purchase_date,
                "equipmentDesc": x.equipmentDesc,
                "purchase_amount": x.purchase_amount,
                "rentalRate": x.rentalRate,
                "plate_number": x.plate_number,
                "status": x.status,
                "project_site": x.project_site,
                "remarks": x.remarks,
                "owner": x.owner,
            }
            for x in equipmentList
        ]
       
    return equipmentData

@tviProject.get("/api-searchID-tiv-equipment/")
async def get_costData_id(id: int,username: str = Depends(validateLogin)):

    equipmentList = getEquipmentTVI()

    equipmentData = [
            {
                "id": x.id,
                "equipmentID": x.equipmentID,
                "purchase_date": x.purchase_date,
                "equipmentDesc": x.equipmentDesc,
                "purchase_amount": x.purchase_amount,
                "rentalRate": x.rentalRate,
                "plate_number": x.plate_number,
                "status": x.status,
                "project_site": x.project_site,
                "remarks": x.remarks,
                "owner": x.owner,
            }
            for x in equipmentList
        ]
      
    new_list = [d['id'] for d in equipmentData]

    # new_dict = {i: d['id'] for i, d in enumerate(equipmentData)}
    # print(new_dict)

    if id not in new_list:
        raise HTTPException(
            status_code=404, detail=f"Equipment with ID no. {id} does not exist"
        )
       

    x = select_tivEquipment_with_id(id=id)


    costData = [

        {
            
            "id": x.id,
            "equipmentID": x.equipmentID,
            "purchase_date": x.purchase_date,
            "equipmentDesc": x.equipmentDesc,
            "purchase_amount": x.purchase_amount,
            "rentalRate": x.rentalRate,
            "plate_number": x.plate_number,
            "status": x.status,
            "project_site": x.project_site,
            "remarks": x.remarks,
            "owner": x.owner,
        
        }
        
    ]

    return costData



@tviProject.put("/api-update-tvi-equipment-sqlModel/")
async def updateTVIEquipment(id: int,items:equipment_details_tvi,username: str = Depends(validateLogin)):

    """This function is for updating Rizal Equipment"""
    updateTVIequipment(equipmentID=items.equipmentID,purchase_date=items.purchase_date,
                        equipmentDesc=items.equipmentDesc,purchase_amount=items.purchase_amount,
                        rentalRate=items.rentalRate,plate_number=items.plate_number,
                        status=items.status,project_site=items.project_site,
                         remarks=items.remarks, owner=items.owner,id=id)

    

    return  {'Messeges':'Data has been Updated'}


#===============================================TVi Rental Frame ==============================================
@tviProject.get("/api-search-autocomplete-tvi-equipment2/")

def autocomplete_tvi_equipment(term: Optional[str]):
    items = getRentalTVI_id(term=term)

    
    suggestions = []
    for item in items:
        suggestions.append(item.equipmentID)
 
    return suggestions


    # data = getRentalTVI_id(term=term)
    
    # costData = [

    #     {
            
    #         # "id": x.id,
    #         "equipmentID": x.equipmentID,
    #         # "purchase_date": x.purchase_date,
    #         # "equipmentDesc": x.equipmentDesc,
    #         # "purchase_amount": x.purchase_amount,
    #         # "rentalRate": x.rentalRate,
    #         # "plate_number": x.plate_number,
    #         # "status": x.status,
    #         # "remarks": x.remarks,
    #         # "owner": x.owner,
        
    #     }
    #     for x in data
    # ]

    # return costData

@tviProject.post("/api-insert-tvi-rental-sqlModel/")
async def insertRentalTvi(items:TVIRentalTransaction,username: str = Depends(validateLogin)):
    """This function is to update employee Details"""
    today = datetime.now()
    insertRental_tvi(transDate=items.transDate,equipmentId=items.equipmentId,
                        totalHours=items.totalHours,rentalRate=items.rentalRate,
                        totalAmount=items.totalAmount,taxRate=items.taxRate,vat_output=items.vat_output,
                        net_of_vat=items.net_of_vat,driverOperator=items.driverOperator,user=username,
                        date_credited=today)


    return  {'Messeges':'Data has been Save'}  

@ tviProject.get('/api-get-tvi-rental-sqlModel/')
def get_RentalData(username: str = Depends(validateLogin)):
    """This function is for querying all Equipment"""
    rentalList = getRentalTVI()

    Data = [
            {
                "id": x.id,
                "transDate ": x.transDate ,
                "equipmentId": x.equipmentId,
                "totalHours": x.totalHours,
                "rentalRate": x.rentalRate,
                "totalAmount": x.totalAmount,
                "taxRate": x.taxRate,
                "vat_output": x.vat_output,
                "net_of_vat": x.net_of_vat,
                "driverOperator": x.driverOperator,
                "user": x.user,
                "date_updated": x.date_updated,
                "date_credited": x.date_credited,
            }
            for x in rentalList
        ]
    
    return Data


@ tviProject.get('/api-get-tvi-all-rentalTransaction-sqlModel/')
def get_RentalData(datefrom,dateto,equipmentId: str,
                     username: str = Depends(validateLogin)):
    """This function is for querying all Equipment"""
    rentalList = getRentalTVI_all(datefrom=datefrom,dateto=dateto,
                                        equipmentId=equipmentId)

    Data = [
            {
                "id": x.id,
                "transDate": x.transDate ,
                "equipmentId": x.equipmentId,
                "totalHours": x.totalHours,
                "rentalRate": x.rentalRate,
                "totalAmount": x.totalAmount,
                "taxRate": x.taxRate,
                "vat_output": x.vat_output,
                "net_of_vat": x.net_of_vat,
                "driverOperator": x.driverOperator,
                "user": x.user,
                "date_updated": x.date_updated,
                "date_credited": x.date_credited,
            }
            for x in rentalList
        ]
    
    return Data




@tviProject.get("/api-search-tvi-equipmentID/")
def search_tvi_equipment_insert(term: Optional[str]):

    data = getRentalTVI_id(term=term)
    
    costData = [

        {
            
            "id": x.id,
            "equipmentID": x.equipmentID,
            "purchase_date": x.purchase_date,
            "equipmentDesc": x.equipmentDesc,
            "purchase_amount": x.purchase_amount,
            "rentalRate": x.rentalRate,
            "plate_number": x.plate_number,
            "status": x.status,
            "remarks": x.remarks,
            "project_site": x.project_site,
            "owner": x.owner,
        
        }
        for x in data
    ]

    

    return costData



@tviProject.get("/api-get-update-tvi-rentalTransaction-sqlModel/{id}", response_class=HTMLResponse)
async def getTviTrans(id: int,request:Request,username: str = Depends(validateLogin)):
    """This function is for querying from Rental Transactions for update purposes"""

    rentalList = getRentalTVI_id_update(id=id)

    Data = [
            {
                "id": x.id,
                "transDate": x.transDate ,
                "equipmentId": x.equipmentId,
                "totalHours": x.totalHours,
                "rentalRate": x.rentalRate,
                "totalAmount": x.totalAmount,
                "taxRate": x.taxRate,
                "vat_output": x.vat_output,
                "net_of_vat": x.net_of_vat,
                "driverOperator": x.driverOperator,
                "project_site": x.project_site,
                "user": x.user,
                "date_updated": x.date_updated,
                "date_credited": x.date_credited,
            }
            for x in rentalList
        ]
    
    
    return templates.TemplateResponse("tvi/tviRentalUpdate.html",{'request':request,'Data':Data})

@tviProject.put("/api-update-tvi-rental-sqlModel/{id}")
async def updateTVIRental(id: int,items:TVIRentalTransaction,username: str = Depends(validateLogin)):

    """This function is for updating Rizal Equipment"""
    today = datetime.now()
    updateTVIrental(transDate=items.transDate,equipmentId=items.equipmentId,
                        totalHours=items.totalHours,rentalRate=items.rentalRate,
                        totalAmount=items.totalAmount,taxRate=items.taxRate,
                        vat_output=items.vat_output,net_of_vat=items.net_of_vat,project_site=items.project_site,
                        driverOperator=items.driverOperator,user=username,
                        date_updated=today,id=id)

    return  {'Messeges':'Data has been Updated'}

#=================================================TVI Diesel Transaction Frame===================================

@tviProject.post("/api-insert-tvi-diesel-sqlModel/")
async def insertDieselTvi(items:TVIDiesel,username: str = Depends(validateLogin)):
    """This function is to update employee Details"""
    today = datetime.now()
    insertDiesel_tvi(transDate=items.transDate,equipmentId=items.equipmentId,
                        withdrawalSlip=items.withdrawalSlip,totalliters=items.totalliters,
                        price=items.price,totalAmount=items.totalAmount,
                        user=username,date_credited=today)


    return  {'Messeges':'Data has been Save'}

from config.tvi_models import getDieselTVI_all
@tviProject.get("/api-search-tvi-diesel-trans/")
def search_tvi_dieseltransAll(datefrom,dateto,equipmentId: Optional[str]):
    """This is for searching all Data from Diesel table"""
    data = getDieselTVI_all(datefrom=datefrom,dateto=dateto,equipmentId=equipmentId)
    
    costData = [

        {
            
            "id": x.id,
            "transDate": x.transDate,
            "equipmentId": x.equipmentId,
            "withdrawalSlip": x.withdrawalSlip,
            "totalliters": x.totalliters,
            "price": x.price,
            "totalAmount":"{:,.2f}".format(x.totalAmount),
            "user": x.user,
            "date_updated": x.date_updated,
            "date_credited": x.date_credited,
            
        
        }
        for x in data
    ]

    return costData

from config.tvi_models import getDieselTVI_id
@tviProject.get("/api-get-update-tvi-dieselTrans-sqlModel/{id}", response_class=HTMLResponse)
async def getTviTrans(id: int,request:Request,username: str = Depends(validateLogin)):
    """This function is for querying from Rental Transactions for update purposes"""

    DieselList = getDieselTVI_id(id=id)

    Data = [
            {
            "id": x.id,
            "transDate": x.transDate,
            "equipmentId": x.equipmentId,
            "withdrawalSlip": x.withdrawalSlip,
            "totalliters": x.totalliters,
            "price": x.price,
            "totalAmount": x.totalAmount,
            "user": x.user,
            "date_updated": x.date_updated,
            "date_credited": x.date_credited,
            }
            for x in DieselList
        ]
    
    # print(Data)
    return templates.TemplateResponse("tvi/tviDieselUpdate.html",{'request':request,'Data':Data})


from config.tvi_models import getDieselTVI_withSlip
@tviProject.get("/api-search-tvi-diesel-withDrawalSlip/")
def search_tvi_dieselWithdrawSlip(withdrawalSlip: Optional[str]):
    """This is for searching all Data from Diesel table"""
    data = getDieselTVI_withSlip(withdrawalSlip=withdrawalSlip)
    
    costData = [

        {
            
            "id": x.id,
            "transDate": x.transDate,
            "equipmentId": x.equipmentId,
            "withdrawalSlip": x.withdrawalSlip,
            "totalliters": x.totalliters,
            "price": x.price,
            "totalAmount":"{:,.2f}".format(x.totalAmount),
            "user": x.user,
            "date_updated": x.date_updated,
            "date_credited": x.date_credited,
            
        
        }
        for x in data
    ]

    return costData

from config.tvi_models import updateTVIDiesel
@tviProject.put("/api-update-tvi-diesel-sqlModel/{id}")
async def updateTVIdiesel(id: int,items:TVIDiesel,username: str = Depends(validateLogin)):

    """This function is for updating Rizal Equipment"""
    today = datetime.now()
    updateTVIDiesel(transDate=items.transDate,equipmentId=items.equipmentId,
                        withdrawalSlip=items.withdrawalSlip,totalliters=items.totalliters,
                        price=items.price,totalAmount=items.totalAmount,
                        user=username,date_updated=today,id=id)

    return  {'Messeges':'Data has been Updated'}





    

# @tviProject.get("/api-search-tiv-test/")
# async def get_costData_id(items:equipment_details_tvi | None = None,username: str = Depends(validateLogin)):
#     equipmentList = getEquipmentTVI2()


#     for i in equipmentList:

#         def checkEquipment(item:i) -> bool:
#             return all(
#                 items.id is None or item.i['id'] == items.id
#             )
    
  
        

   

       
    # result = {}
    # for d in list_of_dicts:
    #     result.update(d)

    #     print(result)

    #     return(result)
    
    
    
   

