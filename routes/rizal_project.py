from traceback import format_list
from fastapi import APIRouter, Body, HTTPException, Depends, Request, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from config.db import mydb


from bson import ObjectId
from typing import Optional

from datetime import timedelta, datetime


from jose import jwt

JWT_SECRET = 'myjwtsecret'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

rizal_project = APIRouter(include_in_schema=False)


templates = Jinja2Templates(directory="templates")


#===========================================Calling for UserName ===========================================
def validateLogin(request:Request):

    try :
        token = request.cookies.get('access_token')
        if token is None:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Not Authorized",
            headers={"WWW-Authenticate": "Basic"},
            )
        else:
            scheme, _, param = token.partition(" ")
            payload = jwt.decode(param, JWT_SECRET, algorithms=ALGORITHM)
        
            username = payload.get("sub")
        

            user =  mydb.login.find({"username":username})

            if user is not None:

                return username

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Not Authorized please Login",
            # headers={"WWW-Authenticate": "Basic"},
        )

from schemas.rizal import Equipment,Equipments 
from config.database import Database
Database.initialize()

#=================================================for Govt Mandatories and Cash advances===========================
@rizal_project.get("/cash-advances/", response_class=HTMLResponse)
def get_cashAdvance_record(request: Request, username: str = Depends(validateLogin)):
    """This function is for querying cash advances"""
    return templates.TemplateResponse("rizal_cash_advance.html",{
                                        "request":request
                                                         })

#======================================================Diesel Frame===========================================
@rizal_project.get("/diesel-consumption-list/", response_class=HTMLResponse)
async def get_diesel_params(request: Request):
    
    return templates.TemplateResponse("rizal_diesel_list.html",{"request":request})

@rizal_project.get("/diesel-consumption/", response_class=HTMLResponse)
def get_record(request: Request, username: str = Depends(validateLogin)):
    """This function is for querying diesel consuption from Rizal Project"""
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

    username = username
    equipment = Equipments(Database.select_allEquipment())
    
    return  templates.TemplateResponse("diesel_consuption.html", 
                                        {"request":request,"agg_result_list":agg_result_list,"equipment":equipment,
                                        "username":username})


@rizal_project.post("/diesel-consumption/", response_class=HTMLResponse)
async def insert_diesel(request: Request, username: str = Depends(validateLogin)):
    form = await request.form()

    trans_date = form.get('trans_date')
    equipment = form.get('equipment')
    withdrawalSlip = form.get('withdrawalSlip')
    liter = form.get('liter')
    price = form.get('price')
    amount = form.get('amount')
    

   
    date_update = datetime.today()
    username = username

   
    try:

        Database.insert_diesel_consuption(transaction_date=trans_date,
                                        equipment_id=equipment,withdrawal_slip=withdrawalSlip,
                                    use_liter=liter,price=price,amount=amount,username=username,date_update=date_update)

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

            equipment = Equipments(Database.select_allEquipment())                           
            return  templates.TemplateResponse("diesel_consuption.html", 
                                            {"request":request,"username":username,"equipment":equipment,
                                            "agg_result_list":agg_result_list})
    except Exception as e:
        print(e)
    equipment = Equipments(Database.select_allEquipment())
    return  templates.TemplateResponse("diesel_consuption.html", 
                                        {"request":request,'equipment':equipment,
                                        "username":username})

@rizal_project.get("/update-diesel/{id}", response_class=HTMLResponse)
def get_updateDiesel(request:Request,id, username: str = Depends(validateLogin)):
    """This function is for dispalying Diesel Transaction using ID"""
    myresult = Database.select_dieselTrans(id=id)
   
    
    agg_result_list = []
    

    id_update = myresult[0]
    transaction_date = myresult[1]
    equipment_id = myresult[2]
    withdrawal_slip = myresult[3]
    use_liter = myresult[4]
    use_liter2 = '{:,.2f}'.format(use_liter)
    price = myresult[5]
    amount = myresult[6]
    amount2 = '{:,.2f}'.format(amount)
    
    user = username
    date_update = datetime.today()

    data={}   
    
    data.update({
        'id': id_update,
        'transaction_date': transaction_date,
        'equipment_id': equipment_id,
        'withdrawal_slip': withdrawal_slip,
        'use_liter': use_liter,
        'price': price,
        'amount': amount,
        'username': user,
        'date_update': date_update
    })

    agg_result_list.append(data)

    return  templates.TemplateResponse("rizal_diesel_consumption_update.html", 
                                        {"request":request,"agg_result_list":agg_result_list,"user":user
                                        })

@rizal_project.post("/update-diesel/{id}", response_class=HTMLResponse)
async def get_updateDiesel(request:Request,username: str = Depends(validateLogin)):
    """This function is for dispalying Diesel Transaction using ID"""
    form = await request.form()
    trans_id = form.get('trans_id')
    trans_date = form.get('trans_date')
    equipment_id = form.get('equipment_id')
    withdrawal_slip = form.get('withdrawal_slip')
    use_liter = form.get('use_liter')
    price = form.get('price')
    amount = form.get('amount')

    

    Database.update_one_diesel(transaction_date=trans_date,
                            equipment_id=equipment_id,withdrawal_slip=withdrawal_slip,
                            use_liter=use_liter,price=price,
                            amount=amount,username=username, id=trans_id)

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
    equipment = Equipments(Database.select_allEquipment())
    return  templates.TemplateResponse("diesel_consuption.html", 
                                        {"request":request,"agg_result_list":agg_result_list,
                                        'equipment':equipment})


#=============================================Rental Transaction ==========================================

from schemas.chartofAccount import chartofAccount,chartofAccounts
@rizal_project.get("/autocomplete-rizal-equipment/")
def autocomplete_rizal_equipment(term: Optional[str]):

    equipmentResult = Database.select_equipment(id=term)
    
    agg_result_list_eqp = []
    for x in equipmentResult:
        
        equipment_id = x[1]
        
        agg_result_list_eqp.append(equipment_id)
       
    return agg_result_list_eqp

@rizal_project.get("/rental-transaction/", response_class=HTMLResponse)
async def get_rental_transaction(request: Request):
    """This function is for displaying rental page """
    

    return  templates.TemplateResponse("rizal_rental.html", 
                                        {"request":request,
                                        })


@rizal_project.post("/rental-transaction/", response_class=HTMLResponse)
async def post_rental_transaction(request: Request, username: str = Depends(validateLogin)):
    """This function is for displaying rental page """

    form = await request.form()
    trans_date = form.get('trans_date')
    term = form.get('equipment')
    total_rental_hour = form.get('total_rental_hour')

    equipmentResult = Database.select_equipment(id=term)
    
    
    for x in equipmentResult:
        rental_rate = x[5]
        
       
        rental_amount = float(rental_rate) * float(total_rental_hour)

        Database.insert_rental_transaction(transaction_date=trans_date,equipment_id=term,
                                        total_rental_hour=total_rental_hour,
                                        rental_rate=rental_rate,rental_amount=rental_amount,
                                        username=username)
        
        
    

    return  templates.TemplateResponse("rizal_rental.html", 
                                        {"request":request
                                        })

@rizal_project.get("/rental-transaction-list/", response_class=HTMLResponse)
async def get_rental_transaction(request: Request):
    """This function is for displaying rental list """

    myresult = Database.select_all_from_rentalDB()


    agg_result_list_eqp = []
    for i in myresult:
        data ={}

        data.update({
            "id": i[0],
            "transaction_date": i[2],
            "equipment_id": i[3],
            "total_rental_hour": i[4],
            "rental_rate": i[5],
            "rental_amount": i[6],
            "username": i[7],
            
        })
        agg_result_list_eqp.append(data)
    

    return  templates.TemplateResponse("rizal_rental_list.html", 
                                        {"request":request,"agg_result_list_eqp":agg_result_list_eqp
                                        })


@rizal_project.get("/rental-search/", response_class=HTMLResponse)
async def get_rentalSearch(request: Request):
    
    return templates.TemplateResponse("rental_list.html",{"request":request})


@rizal_project.get("/13thMonth-computation/", response_class=HTMLResponse)
async def get_13thMonth(request: Request):
    
    return templates.TemplateResponse("comp13thMonth.html",{"request":request})