from fastapi import APIRouter, Body, HTTPException, Depends, Request, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Union, List, Optional
from datetime import datetime, date

from schemas.user import usersEntity

from models.model import SgmcEquipment, RentalSgmc, DieselSGMC, CostSGMC_model
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
    user =  mydb.access_setting.find({"username":username})
    for i in user:
        if i['site'] == 'admin' or i['site'] == 'sgmc':
            return templates.TemplateResponse("sgmc/sgmc_transaction.html", {"request":request}) 
        # error message if not autorized for this transaction
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= "Not Authorized",
               
                )

@sgmcRouter.post("/insert-equipment-sgmc/")
async def insert_rental_sgmc(items:SgmcEquipment, username: str = Depends(ValidationLogin)):
    """This function is for inserting equipment to GRC table"""
    user =  mydb.access_setting.find({"username":username})
    for i in user:
        if i['site'] == 'admin' or i['site'] == 'sgmc' and i['site_transaction_write'] \
                and i['site_transaction_read']:
            try:
                SGMCViews.insert_equipment_sgmc(equipment_id=items.equipment_id,equipmentDiscription=items.equipmentDiscription,
                                                rentalRate=items.rentalRate, comments=items.comments,owners=items.owners,
                                                user=username,date_credited=datetime.now())

                return('Data has been Save')

            except Exception as e:
                error_message = str(e)  # Use the actual error message from the exception
            
                return {"error": error_message}
        # error message if not autorized for this transaction
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= "Not Authorized",
               
                )

@sgmcRouter.get("/api-search-autocomplete-sgmc-equipment/")
def autocomplete_grc_equipment(term: Optional[str] = None): # this is for autocomplete of equipment

    # Ensure you're correctly handling query parameters, 'term' in this case

    equipment = SGMCViews.getEquipment()

    if term:
        filtered_equipment = [item for item in equipment if term.lower() in item.equipment_id.lower()]
    else:
        filtered_equipment = []

    suggestions = [{"value": item.equipment_id,"rentalRate": item.rentalRate,"id":item.id} for item in filtered_equipment]
    return suggestions

@sgmcRouter.post("/api-insert-sgmc-rental/")
async def insert_rental_GRC(items:RentalSgmc, username: str = Depends(ValidationLogin)):
    """This function is for inserting rental for  SGMC  table"""
    user =  mydb.access_setting.find({"username":username})
    for i in user:
        if i['site'] == 'admin' or i['site'] == 'sgmc' and i['site_transaction_write'] \
                and i['site_transaction_read']:
            try:
                SGMCViews.insert_rental_sgmc(transDate=items.transDate,eur=items.eur,equipment_id=items.equipment_id,
                                            timeIn=items.timeIn,timeOut=items.timeOut,totalHours=items.totalHours,
                                                rentalRate=items.rentalRate,amount=items.amount,
                                                    shift=items.shift,driver_operator=items.driver_operator,user=username,
                                                    date_credited=datetime.now)

                return('Data has been Save')

            except Exception as e:
                error_message = str(e)  # Use the actual error message from the exception
            
                return {"error": error_message}
        # error message if not autorized for this transaction
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= "Not Authorized",
               
                )
    
@sgmcRouter.get("/api-get-sgmc-rental-transaction/")
async def getRental_views(datefrom: Optional[date],dateto:Optional[date],equipment_id: Optional[str],
                            username: str = Depends(ValidationLogin))->List:
    """This function is to update employee Details"""
    user =  mydb.access_setting.find({"username":username})
    for i in user:
        if i['site'] == 'admin' or i['site'] == 'sgmc' and i['site_transaction_read']:

            results = SGMCViews.getRental(datefrom=datefrom,dateto=dateto,equipment_id=equipment_id)

            rentalData = [
                
                    {
                    "id": x. id,
                        "transDate": x.transDate,
                        "eur": x.eur,
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
        # error message if not autorized for this transaction
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= "Not Authorized",
               
                )


@sgmcRouter.get("/api-get-sgmc-rental-report-list/")
async def getRental_views(datefrom: Optional[date],dateto:Optional[date],
                            username: str = Depends(ValidationLogin))->List:
    """This function is to update employee Details"""
    user =  mydb.access_setting.find({"username":username})
    for i in user:
        if i['site'] == 'admin' or i['site'] == 'sgmc' and i['site_transaction_read']:

            results = SGMCViews.getRental_report(datefrom=datefrom,dateto=dateto)
            # running_balance = 0
            # rentalData = []
            # for x in results:
            #     # running_balance+=x.totalHours
            #     data={}
            #     data.update({
                        
            #             "equipment_id": x.equipment_id,  
            #             "totalHours": x.totalHours,
            #             "running_balance": running_balance + x['totalHours']
            #         })
            #     rentalData.append(data)
            

            # rentalData = [
            #         {
            #             "equipment_id": x.equipment_id,
            #             "totalHours": x.totalHours,
            #         }
            #         for x in results
            #     ]

            # # Calculate running balance
            # running_balance = 0
            # for entry in rentalData:
            #     entry['running_balance'] = running_balance + entry['totalHours']
            #     running_balance = entry['running_balance']

            rentalData = [
                {
                    "equipment_id": x.equipment_id,
                    "totalHours": x.totalHours,
                }
                for x in results
            ]

            # Calculate running total of totalHours
            total_hours_running_total = sum(entry['totalHours'] for entry in rentalData)

            return {"rentalData": rentalData, "totalHoursRunningTotal": total_hours_running_total}
                
        
            return rentalData
        # error message if not autorized for this transaction
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= "Not Authorized",
               
                )

    

@sgmcRouter.get("/update-rental-sgmc/{id}", response_class=HTMLResponse)
async def grc_template(id:Optional[int],request: Request, username: str = Depends(ValidationLogin)):

    user =  mydb.access_setting.find({"username":username})
    for i in user:
        if i['site'] == 'admin' or i['site'] == 'sgmc' and i['site_transaction_write']:

            results = SGMCViews.getRental_id(item_id=id)

            rentalData = [
                
                    {
                    "id": results.id,
                        "transDate": results.transDate,
                        "eur": results.eur,
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
            
        
            return templates.TemplateResponse("sgmc/sgmc_update_rental.html", {"request":request,"rentalData":rentalData})
        # error message if not autorized for this transaction
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= "Not Authorized",
               
                )
    
@sgmcRouter.put("/api-update-rental-sgmc/{id}")
async def updateGRCRental(id,items:RentalSgmc,username: str = Depends(ValidationLogin)):
    """This function is to update Rental"""
    user =  mydb.access_setting.find({"username":username})
    for i in user:
        if i['site'] == 'admin' or i['site'] == 'sgmc' and i['site_transaction_write']:
            today = datetime.now()
            try:
                SGMCViews.updateRental(transDate=items.transDate,eur=items.eur,equipment_id=items.equipment_id,
                                        timeIn=items.timeIn,timeOut=items.timeOut,
                                        totalHours=items.totalHours,rentalRate=items.rentalRate,
                                        amount=items.amount,shift=items.shift,driver_operator=items.driver_operator,
                                        user=username,date_updated=today,item_id=id)

            except Exception as e:
                error_message = str(e)  # Use the actual error message from the exception
            
                return {"error": error_message}


            return  {'Messeges':'Data has been Updated'}
        # error message if not autorized for this transaction
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= "Not Authorized",
                
                )

@sgmcRouter.post("/api-insert-diesel-sgmc/")
async def insert_diesel_sgmc(items:DieselSGMC, username: str = Depends(ValidationLogin) ): # this function is for inserting diesel 
    user =  mydb.access_setting.find({"username":username})
    for i in user:
        if i['site'] == 'admin' or i['site'] == 'sgmc' and i['site_transaction_write']:
            try:
                SGMCViews.insert_diesel_sgmc(transDate=items.transDate,withdrawal_slip=items.withdrawal_slip,
                                             equipment_id=items.equipment_id,literUse=items.literUse,
                                             price=items.price,amount=items.amount,
                                             user=username,date_credited=datetime.now())

                return('Data has been Save')

            except Exception as e:
                error_message = str(e)  # Use the actual error message from the exception
            
                return {"error": error_message}
            
    # error message if not autorized for this transaction
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Not Authorized",
            
            )


@sgmcRouter.get("/api-get-sgmc-diesel-transaction/")
async def get_update_diesel_views(datefrom: Optional[date],dateto:Optional[date],equipment_id: Optional[str],
                            username: str = Depends(ValidationLogin))->List:
    """This function is to update employee Details"""
    user =  mydb.access_setting.find({"username":username})
    for i in user:
        if i['site'] == 'admin' or i['site'] == 'sgmc' and i['site_transaction_read']:

            results = SGMCViews.get_diesel(datefrom=datefrom,dateto=dateto,equipment_id=equipment_id)

            dieselData = [
                
                    {
                    "id": diesel_data. id,
                        "transDate": diesel_data.transDate,
                        "withdrawal_slip": diesel_data.withdrawal_slip,
                        "equipment_id": equipment_data.equipment_id,
                        "literUse": diesel_data.literUse,
                        "price": diesel_data.price,
                        "amount": diesel_data.amount,
                        "user": diesel_data.user,
                        "date_credited": diesel_data.date_credited,
                       

                    
                    }
                    for diesel_data,equipment_data in results
                ]
            
        
            return dieselData
        # error message if not autorized for this transaction
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= "Not Authorized",
               
                )
    

@sgmcRouter.get("/update-diesel-sgmc/{id}", response_class=HTMLResponse)
async def grc_update_diesel_api(id:Optional[int],request: Request, username: str = Depends(ValidationLogin)):
    user =  mydb.access_setting.find({"username":username})
    for i in user:
        if i['site'] == 'admin' or i['site'] == 'sgmc' and i['site_transaction_read']:

            results = SGMCViews.getDiesel_id(item_id=id)
            print(results)
            dieselData = [
                
                    {
                    "id": diesel_data. id,
                        "transDate": diesel_data.transDate,
                        "withdrawal_slip": diesel_data.withdrawal_slip,
                        "equipment_id": equipment_data.equipment_id,
                        "literUse": diesel_data.literUse,
                        "price": diesel_data.price,
                        "amount": diesel_data.amount,
                        "user": diesel_data.user,
                        "date_credited": diesel_data.date_credited,
                        "equipment_id_id": equipment_data.id,

                    
                    }
                    for diesel_data,equipment_data in results
            ]
            
            print(dieselData)
        
            return templates.TemplateResponse("sgmc/sgmc_update_diesel.html", {"request":request,"dieselData":dieselData})

        # error message if not autorized for this transaction
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= "Not Authorized",
               
                )   


@sgmcRouter.put("/api-update-diesel-sgmc/{id}")
async def updateGRCRental(id,items:DieselSGMC,username: str = Depends(ValidationLogin)):
    """This function is to update Rental"""
    today = datetime.now()
    try:
        SGMCViews.updateDiesel(transDate=items.transDate,withdrawal_slip=items.withdrawal_slip,
                               equipment_id=items.equipment_id,literUse=items.literUse,
                              price=items.price,amount=items.amount,user=username,
                              date_updated=today,item_id=id)
    except Exception as e:
        error_message = str(e)  # Use the actual error message from the exception
    
        return {"error": error_message}


    return  {'Messeges':'Data has been Updated'}  


@sgmcRouter.post("/api-insert-cost-sgmc/")
async def insert_cost_sgmc(items:CostSGMC_model, username: str = Depends(ValidationLogin) ): # this function is for inserting diesel 
    user =  mydb.access_setting.find({"username":username})
    for i in user:
        if i['site'] == 'admin' or i['site'] == 'sgmc' and i['site_transaction_write']:
            try:
                SGMCViews.insert_cost_sgmc(transDate=items.transDate,equipment_id=items.equipment_id,
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


@sgmcRouter.get("/api-get-sgmc-cost-transaction/")
async def get_update_diesel_views(datefrom: Optional[date],dateto:Optional[date],equipment_id: Optional[str],
                            username: str = Depends(ValidationLogin))->List:
    """This function is to update employee Details"""
    user =  mydb.access_setting.find({"username":username})
    for i in user:
        if i['site'] == 'admin' or i['site'] == 'sgmc' and i['site_transaction_read']:

            results = SGMCViews.get_cost(datefrom=datefrom,dateto=dateto,equipment_id=equipment_id)

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
                       

                    
                    }
                    for cost_data,equipment_data in results
                ]
            
        
            # return dieselData

            # Calculate running total of totalHours
            total_amount = sum(entry['amount'] for entry in costData)
            total_amount2 = '{:,.2f}'.format(total_amount)

            return {"costData": costData, "totalAmount": total_amount2}
        # error message if not autorized for this transaction
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= "Not Authorized",
               
                )


@sgmcRouter.get("/update-cost-sgmc/{id}", response_class=HTMLResponse)
async def grc_update_diesel_api(id:Optional[int],request: Request, username: str = Depends(ValidationLogin)):
    user =  mydb.access_setting.find({"username":username})
    for i in user:
        if i['site'] == 'admin' or i['site'] == 'sgmc' and i['site_transaction_write']:

            results = SGMCViews.getcost_id(item_id=id)
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
        
            return templates.TemplateResponse("sgmc/sgmc_update_cost.html", {"request":request,"costData":costData})

        # error message if not autorized for this transaction
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= "Not Authorized",
               
                )   

    
@sgmcRouter.put("/api-update-cost-sgmc/{id}") # this is to update cost
async def update_cost_sgmc(id,items:CostSGMC_model,username: str = Depends(ValidationLogin)):
    """This function is to update Rental"""
    today = datetime.now()
    try:
        SGMCViews.updateCost(transDate=items.transDate,equipment_id=items.equipment_id,
                                cost_details=items.cost_details,amount=items.amount,
                                particular=items.particular,user=username,
                                date_updated=datetime.now(),item_id=id)
    except Exception as e:
        error_message = str(e)  # Use the actual error message from the exception
    
        return {"error": error_message}


    return  {'Messeges':'Data has been Updated'}  
