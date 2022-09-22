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
            detail= e,
            headers={"WWW-Authenticate": "Basic"},
        )


      

from config.database import Database,Database2
db = Database() # calling database function or connection for mysql data from Linode
@rizal_project.get("/diesel-consumption/", response_class=HTMLResponse)
def get_record(request: Request, username: str = Depends(validateLogin)):
    """This function is for querying diesel consuption from Rizal Project"""
    allConsumption = db.query(query=f"SELECT * FROM diesel_consumption")
    
    allconsuption2 = allConsumption['result']

    agg_result_list = []
    for x in allconsuption2:

        transaction_date = x['transaction_date']
        equipment_id = x['equipment_id']
        use_liter = x['use_liter']
        use_liter2 = '{:,.2f}'.format(use_liter)
        price = x['price']
        amount = x['amount']
        amount2 = '{:,.2f}'.format(amount)
        
        

        data={}   
        
        data.update({
            'transaction_date': transaction_date,
            'equipment_id': equipment_id,
            'use_liter': use_liter2,
            'price': price,
            'amount': amount2,
        })

        agg_result_list.append(data)

    username = username
    
    return  templates.TemplateResponse("diesel_consuption.html", 
                                        {"request":request,"agg_result_list":agg_result_list,"username":username})

Database2.initialize()
@rizal_project.post("/diesel-consumption/", response_class=HTMLResponse)
async def insert_diesel(request: Request, username: str = Depends(validateLogin)):
    form = await request.form()

    trans_date = form.get('trans_date')
    equipment = form.get('equipment')
    withdrawalSlip = form.get('withdrawalSlip')
    liter = form.get('liter')
    price = form.get('price')
    amount = form.get('amount')
    user_name = form.get('username')
   
    username = username

    # dataInsert = db.query(
    #                 query=f"""INSERT INTO diesel_consumption (transaction_date, equipment_id, 
    #                 withdrawal_slip, use_liter, price,amount, username)
    #                  VALUES ({trans_date}, {equipment}, {withdrawalSlip}, {liter}, {price},{amount}, {user_name})
    #     """,
    #     autoCommit=True,
    # )
   
    # return dataInsert
    try:

        Database2.insert_diesel_consuption(transaction_date=trans_date,
                                        equipment_id=equipment,withdrawal_slip=withdrawalSlip,
                                    use_liter=liter,price=price,amount=amount,username=user_name)
    except Exception as e:
        print(e)

    return  templates.TemplateResponse("diesel_consuption.html", 
                                        {"request":request,"username":username})


