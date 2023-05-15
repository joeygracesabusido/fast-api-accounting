from traceback import format_list
from fastapi import APIRouter, Body, HTTPException, Depends, Request, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from config.db import mydb
# from config.db import worker
from models.model import EmployeeReg, RizalTonnagehaul
from fastapi import staticfiles

from bson import ObjectId
from typing import Optional

from datetime import timedelta, datetime

from models.model import EquipmentDetails


from jose import jwt

JWT_SECRET = 'myjwtsecret'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

rizal_project = APIRouter(include_in_schema=False)


templates = Jinja2Templates(directory="templates")



#===========================================Calling for UserName ===========================================

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


@rizal_project.get('/payroll-computation/', response_class=HTMLResponse)
def get_payrollComputation(request: Request,  username: str = Depends(validateLogin)):
    """This function is for displaying """

    return templates.TemplateResponse("payroll_computation.html",{
                                                "request": request
                                                        })
from config.models import getSSSTable
@rizal_project.get('/sss-computation/')
def get_payrollComputation(username: str = Depends(validateLogin)):
    """This function is for displaying """
    result = getSSSTable()


    rentalData = [
        
            {
                "amountFrom": i.amountFrom,
                "amountTo": i.amountTo,
                "empShare": i.empShare,
                "mandtoryProvi": i.mandtoryProvi
               
            }
           for i in result
        ]
    return rentalData


#============================================Payroll Transaction ==================================

@rizal_project.get("/payroll-transaction-adminlogin/", response_class=HTMLResponse)
def get_payrollTransaction(request: Request, username: str = Depends(validateLogin)):
    """This function is for querying cash advances"""
    # data = getPayrollTransactions(datefrom=datefrom,dateto=dateto,department=department)
    
   
    # payrollData = [
        
    #         {
               
    #             "id": i['id'],
    #             "employee_id": i['employee_id'],
    #             "position_name": i['position_name'],
    #             "name":i['firstname'] + ',' + i['firstname'],
    #             "salary_rate": i['salary_rate'],
    #             "grosspay_save": i['grosspay_save'],
    #             "department": i['department'],
    #             "totalDem_save": i['totalDem_save'],
    #             "otherforms_save": i['otherforms_save'],
    #             "taxable_amount": i['taxable_amount'],
    #             "total_mandatory": i['total_mandatory'],
    #             "taxable_mwe_detail": i['taxable_mwe_detail'],
    #             "sss_save": i['sss_save'],
    #             "phic_save": i['phic_save'],
    #             "hmdf_save": i['hmdf_save'],
    #             "cut_off_date": i['cut_off_date'],
                
    #             # "equipmentID": i['equipment_id']
            
    #         }
    #       for i in data
    #     ]
    

   

    return templates.TemplateResponse("ho/payroll_list.html",{
                                        "request":request
                                                         })

from config.models import getPayrollTransactions
@rizal_project.get("/api-payroll-transaction-AdminLogin/")
async def get_employee_payroll(datefrom,dateto,on_off_details:Optional[str], department:Optional[str],username: str = Depends(validateLogin)):
    """This function is for queryong for Payroll transactions"""

    data = getPayrollTransactions(datefrom=datefrom,dateto=dateto,department=department,on_off_details=on_off_details)
    
   
    costData = [
        
            {
               
                "id": i['id'],
                "employee_id": i['employee_id'],
                "position_name": i['position_name'],
                "name":i['last_name'] + ',' + i['first_name'],
                "salary_rate": i['salary_rate'],
                "grosspay_save": i['grosspay_save'],
                "department": i['department'],
                "totalDem_save": i['totalDem_save'],
                "otherforms_save": i['otherforms_save'],
                "taxable_amount": i['taxable_amount'],
                "total_mandatory": i['total_mandatory'],
                "taxable_mwe_detail": i['taxable_mwe_detail'],
                "sss_save": i['sss_save'],
                "phic_save": i['phic_save'],
                "hmdf_save": i['hmdf_save'],
                "cut_off_date": i['cut_off_date'],
                
                # "equipmentID": i['equipment_id']
            
            }
          for i in data
        ]
    

    return costData

                                                         


#======================================================Diesel Frame===========================================
@rizal_project.get("/diesel-consumption-list/", response_class=HTMLResponse)
async def get_diesel_params(request: Request,username: str = Depends(validateLogin)):
    
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
            'withdrawal_slip': x[3],
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
                'withdrawal_slip': x[3],
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
async def get_rental_transaction(equipment_id,request: Request,username: str = Depends(validateLogin)):
    """This function is for displaying rental list """

    myresult = Database.select_all_from_rentalDB(equipment_id=equipment_id)


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
async def get_rentalSearch(request: Request,username: str = Depends(validateLogin)):
    
    return templates.TemplateResponse("rental_list.html",{"request":request})







@rizal_project.get("/get_employee_payroll/", response_class=HTMLResponse)
async def get_employee_payroll(request: Request,username: str = Depends(validateLogin)):
    
    return templates.TemplateResponse("rizal/employee_transaction.html",{"request":request})

from config.models import updateRentalRizal,getallRental_id
@rizal_project.get("/update-rental-rizal/{id}", response_class=HTMLResponse)
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
    
   
   
    return templates.TemplateResponse("rizal/updateRizalRental.html",{"request":request,"rentalData":rentalData})

from models.model import RizalRental
@rizal_project.put("/update-rental-rizal/{id}")
async def updateRizalRental(id,items:RizalRental,username: str = Depends(validateLogin)):
    """This function is to update Cost"""
    today = datetime.now()

    updateRentalRizal(transaction_date=items.transaction_date,equipment_id=items.equipment_id,
                            total_rental_hour=items.total_rental_hour, rental_rate=items.rental_rate,rental_amount=items.rental_amount,
                             username=username,date_update=today,eur_form=items.eur_form, id=id)

    return  {'Messeges':'Data has been Updated'}


#=============================================This is for employee Transaction===========================================
from config.database import Database

Database.initialize()
@rizal_project.get("/13thMonth-computation/", response_class=HTMLResponse)
async def get_13thMonth(request: Request,username: str = Depends(validateLogin)):
    
    return templates.TemplateResponse("comp13thMonth.html",{"request":request})

@rizal_project.get("/employee-registration/", response_class=HTMLResponse)
async def get_employee_payroll(request: Request,username: str = Depends(validateLogin)):
    
    return templates.TemplateResponse("rizal/employeeReg.html",{"request":request})

@rizal_project.get("/api-employee-registration/")
async def get_employee_payroll(employee_id,username: str = Depends(validateLogin)):

    employeelList = Database.get_employee_info(employee_id=employee_id)
    # print(employeelList)

    employeeData = [
            {
                "id": x[0],
                "employee_id": x[1],
                "lastName": x[2],
                "firstName": x[3],
                "middleName": x[4],
                "gender": x[5],
                "address_employee": x[6],
                "contactNumber": x[7],
                "contact_person": x[8],
                "emer_cont_person": x[9],
                "position": x[10],
                "date_hired": x[11],
                "department": x[12],
                "end_contract": x[13],
                "tin": x[14],
                "sssNumber": x[15],
                "phicNumber": x[16],
                "hdmfNumber": x[17],
                "employment_status": x[18],
                "update_contract": x[19],
                "salary_rate": x[20],
                "taxCode": x[21],
                "Salary_Detail": x[22],
                "off_on_details": x[23]

            }
            for x in employeelList
        ]
    
    
       
    return employeeData
    
@rizal_project.put("/api-update-employee/{id}")
async def get_employee_payroll(id,items:EmployeeReg,username: str = Depends(validateLogin)):
    """This function is to update employee Details"""
    today = datetime.today()

    Database.updateEmployeeDetails(lastName=items.lastName,firstName=items.firstName,
                                    middleName=items.middleName,gender=items.gender,address_employee=items.address_employee,
                                    contactNumber=items.contactNumber,contact_person=items.contact_person,
                                    emer_cont_person=items.emer_cont_person,position=items.position,
                                    date_hired=items.date_hired,department=items.department,
                                    end_contract=items.end_contract,tin=items.tin,
                                    sssNumber=items.sssNumber,phicNumber=items.phicNumber,hdmfNumber=items.hdmfNumber,
                                    employment_status=items.employment_status,
                                    salary_rate=items.salary_rate,taxCode=items.taxCode,off_on_details=items.off_on_details,
                                    Salary_Detail=items.Salary_Detail,user=username,update_date=today,id=id)

    return  {'Messeges':'Data has been updated'}



@rizal_project.get("/employee-list/", response_class=HTMLResponse)
async def get_all_employee(request: Request,username: str = Depends(validateLogin)):
    
    return templates.TemplateResponse("ho/employeeList.html",{"request":request})

@rizal_project.get("/api-employee-list/")
async def get_employee_payroll(department,username: str = Depends(validateLogin)):

    employeelList = Database.get_employeeDepartment(department=department)
    # print(employeelList)

    employeeData = [
            {
                
                "employee_id": x[0],
                "lastName": x[1],
                "firstName": x[2],
                "position": x[3],
                "department": x[4],
                "off_on_details": x[5],
                "employment_status": x[6],
                "date_hired": x[7]

            }
            for x in employeelList
        ]
       
    return employeeData

#================================================HAULING BILLING ========================================
@rizal_project.get("/insert-tonnage-rizal/", response_class=HTMLResponse)
async def insert_tonnage_rizal(request: Request,username: str = Depends(validateLogin)):
    """This is to display html page for inserting Tonnage"""
    return templates.TemplateResponse("rizal/tonnage_insert.html",{"request":request})

@rizal_project.post("/api-insert-tonnage-rizal/")
async def insertTonnageHauling(items:RizalTonnagehaul,username: str = Depends(validateLogin)):
    """This function is to update employee Details"""
    today = datetime.now()

    Database.insertTonnagehauling(transDate=items.transDate,equipment_id=items.equipment_id,
                                    tripTicket=items.tripTicket,totalTrip=items.totalTrip,
                                    totalTonnage=items.totalTonnage,
                                    rate=items.rate,amount=items.amount,driverOperator=items.driverOperator,
                                    user=username,date_credited=today)

    return  {'Messeges':'Data has been Save'}

@rizal_project.get("/api-search-autocomplete-equipment-rizal/")
def autocomplete_equipmentID(term: Optional[str]):
    items = Database.select_allEquipment_autocomplete(equipment_id=term)

    suggestions = []
    for item in items:
        suggestions.append(item[1])
        
    return suggestions


@rizal_project.get("/api-tonnage-hauling-list/")
async def getTonnageList(datefrom,dateto,equipment_id,username: str = Depends(validateLogin)):

    tonnageList = Database.get_tonnageHaul(datefrom=datefrom,dateto=dateto,equipment_id=equipment_id)
    # print(tonnageList)

    tonnageData = [
        
            {
                
                "id": x[0],
                "transDate": x[1],
                "equipment_id": x[2],
                "tripTicket": x[3],
                "totalTrip": x[4],
                "totalTonnage": x[5],
                "rate": x[6],
                "amount": "{:,.2f}".format(x[7]),
                "driverOperator": x[8]
                

            }
            for x in tonnageList
        ]
       
    return tonnageData


@rizal_project.get("/update-tonnageHaul/{id}", response_class=HTMLResponse)
def get_updatetonnageHaul(request:Request,id, username: str = Depends(validateLogin)):
    """This function is for dispalying Diesel Transaction using ID"""
    myresult = Database.get_tonnageHaulID(id=id)


    tonnageData = [
        
            {

                "id": x[0],
                "transDate": x[1],
                "equipment_id": x[2],
                "tripTicket": x[3],
                "totalTrip": x[4],
                "totalTonnage": x[5],
                "rate": x[6],
                "amount": "{:,.2f}".format(x[7]),
                "driverOperator": x[8]
            

            }
            for x in myresult
        ]

  
   
    
    

    return  templates.TemplateResponse("rizal/updateTonnage.html", 
                                        {"request":request,"tonnageData":tonnageData,"user":username
                                        })

@rizal_project.put("/api-update-tonnageHaul/{id}")
async def get_employee_payroll(id,items:RizalTonnagehaul,username: str = Depends(validateLogin)):
    """This function is to update employee Details"""
    today = datetime.today()

    Database.updateTonnageRizal(transDate=items.transDate,equipment_id=items.equipment_id,
                                    tripTicket=items.tripTicket,totalTrip=items.totalTrip,
                                    totalTonnage=items.totalTonnage,
                                    rate=items.rate,amount=items.amount,driverOperator=items.driverOperator,
                                    user=username,date_updated=today,id=id)

    return  {'Messeges':'Data has been updated'}


#=================================================for HO Frame============================================
@rizal_project.get("/home/", response_class=HTMLResponse)
async def get_all_employee(request: Request):
    
    return templates.TemplateResponse("ho/home.html",{"request":request})

@rizal_project.get("/api-employee-list-per-count/")
async def get_employee_payroll(department,username: str = Depends(validateLogin)):
    """This function is to get number of Employee"""

    employeelList = Database.get_totalNumberEmployee(department=department)
    # print(employeelList)
 
    return employeelList

@rizal_project.get("/api-employee-list-per-count-off/")
async def get_employee_payroll(department,username: str = Depends(validateLogin)):
    """This function is to get number of Employee"""

    employeelList = Database.get_totalNumberEmployee_off(department=department)
    
  
    return employeelList


#===========================================For cost Analysis Frame==============================================

@rizal_project.get("/api-tonnage-cost/")
async def getTonnageList(datefrom,dateto,username: str = Depends(validateLogin)):

    
    
    rentalList = Database.get_rental_cost(datefrom=datefrom,dateto=dateto)

    

    totalHours = 0
    totalAmount = 0

    totalTrip = 0
    totalTonnage = 0
    amount = 0

    agg_result_list = []
    for y in rentalList:
        transaction_date = y[0],
        equipment_id = y[1],
        totalHours = y[2],
        totalAmount = y[3],

        tonnageList = Database.get_ton_cost(datefrom=datefrom,dateto=dateto) # for hauling_tonnage table
       
        dieselList = Database.get_diesel_cost(datefrom=datefrom,dateto=dateto)

        for x in tonnageList:
            transDate = x[0],
            equipment_id2 = x[1],
            totalTrip = x[2],
            totalTonnage = x[3],
            amount = x[4],

            if equipment_id == equipment_id2:
                totalHours = y[2],
                totalAmount = y[3],
                totalTonnage = x[3],
                totalTrip = x[2],
                amount = x[4],

                totalService = totalAmount + amount


            
            

        for d in dieselList:
            equipment_id3 = d[0]
            
            totalLtrs = d[1]
            totalAmountDiesel = d[2]

            print(totalLtrs)
            if equipment_id == equipment_id3:
                totalLtrs = d[1]
                totalAmountDiesel = d[2]
                
        
                data ={}

                data.update({
                    "Date": transDate,
                    "equipment_id": equipment_id,
                    "totalAmount": totalAmount,
                    "amount": amount,
                    "totalIncome":totalService,
                    "totalLiters": totalLtrs,
                    "totalAmountDiesel": totalAmountDiesel})
                agg_result_list.append(data)

    # tonnageData = [
        
    #         {
                
                
    #             "transDate": x[0],
    #             "equipment_id": x[1],
    #             "totalTrip": x[2],
    #             "totalTonnage": x[3],
    #             "amount": "{:,.2f}".format(x[4]),
                
                

    #         }
    #         for x in tonnageList
    #     ]
       
    return agg_result_list

@rizal_project.get("/api-tonnage-cost-analysis/")
async def getCostAnalysis(datefrom,dateto,username: str = Depends(validateLogin)):
    """This function is for cost  analysis"""

    cost = Database.get_costAnalysis(datefrom=datefrom,dateto=dateto)
    # print(cost)

    costData = [
        
            {
                 
                "equipment_id": x[0],
                "TonnageAmount": "{:,.2f}".format(x[1]),
                "RentalAmount": "{:,.2f}".format(x[2]),
                "DieselAmount": "{:,.2f}".format(x[3]),
                "Expenses": "{:,.2f}".format(x[4]),
                "netIncome": "{:,.2f}".format(float(((x[1])+(x[2]))-x[3]-x[4])),
            
            }
            for x in cost
        ]

    return costData

#================================================Rizal Cost Frame=====================================

from config.models import (cost,equipment_details, insertCost,select_cost,
                            select_cost_id,update_cost,select_test,
                            selectCostAnalysis2,getEquipmentRizal,insertEquipment,
                            select_rizalEquipment_id,updateRizalequipment
                            )
from models.model import Cost
@rizal_project.get("/api-insert-rizal-cost/", response_class=HTMLResponse)
async def get_all_employee(request: Request):
    
    return templates.TemplateResponse("rizal/insertCost.html",{"request":request})



@rizal_project.post("/api-insert-rizal-cost/")
async def insertCostapi(items:Cost,username: str = Depends(validateLogin)):
    """This function is to update employee Details"""
    today = datetime.now()

    insertCost(transDate=items.transDate,equipment_id=items.equipment_id,salaries=items.salaries,
                    fuel=items.fuel,oil_lubes=items.oil_lubes, 
                    mechanicalSupplies=items.mechanicalSupplies,
                    repairMaintenance=items.repairMaintenance,meals=items.meals,
                    transpo=items.transpo,tires=items.tires,amortization=items.amortization,
                    others=items.others, totalAmount=items.totalAmount,user=username,date_created=today)

    return  {'Messeges':'Data has been Save'}

@rizal_project.get("/api-get-rizal-cost/")
async def get_cost(datefrom,dateto,equipment_id,username: str = Depends(validateLogin)):
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


@rizal_project.get("/update-cost-rizal/{id}", response_class=HTMLResponse)
async def get_costData_id(id,request: Request):

    results = select_cost_id(id=id)
    

    costData = [
        
            {
                "id": results.id,
                "transDate": results.transDate,
                "equipment_id": results.equipment_id,
                "salaries": results.salaries,
                "fuel": results.fuel,
                "oil_lubes": results.oil_lubes,
                "mechanicalSupplies": results.mechanicalSupplies,
                "repairMaintenance": results.repairMaintenance,
                "meals": results.meals,
                "transpo": results.transpo,
                "tires": results.tires,
                "amortization": results.amortization,
                "others": results.others,
                "totalAmount": results.totalAmount
            
            }
           
        ]
    

    # return costData


    # cost = Database.get_cost_id(id=id)

    # costData = [
        
    #         {
    #              "id": results[0],
    #             "transDate": results[1],
    #             "equipment_id": results[2],
    #             "salaries": results[3],
    #             "fuel": results[4],
    #             "oil_lubes": results[5],
    #             "mechanicalSupplies": results[6],
    #             "repairMaintenance": results[7],
    #             "meals": results[8],
    #             "transpo": results[9],
    #             "tires": results[10],
    #             "amortization": results[11],
    #             "others": results[12],
    #             "totalAmount": results[13]
            
    #         }
    #        for results in cost
    #     ]
    
    return templates.TemplateResponse("rizal/updateCost.html",{"request":request,"results":costData})


@rizal_project.put("/api-update-rizal-cost/{id}")
async def updateCostapi(id,items:Cost,username: str = Depends(validateLogin)):
    """This function is to update Cost"""
    today = datetime.now()

    update_cost(transDate=items.transDate,equipment_id=items.equipment_id,salaries=items.salaries,
                    fuel=items.fuel,oil_lubes=items.oil_lubes, 
                    mechanicalSupplies=items.mechanicalSupplies,
                    repairMaintenance=items.repairMaintenance,meals=items.meals,
                    transpo=items.transpo,tires=items.tires,amortization=items.amortization,
                    others=items.others, totalAmount=items.totalAmount,user=username,date_update=today,id=id)

    return  {'Messeges':'Data has been Updated'}

@rizal_project.get("/api-test-sum/")
async def test(username: str = Depends(validateLogin)):
    """This function is for testing"""


    data = select_test()
    
   
    costData = [
        
            {
               
                "equipment_id": i['equipment_id'],
                "salaries": i['salaries'],
                "fuel": i['fuel'],
                "oil_lubes": i['oil_lubes'],
                "mechanicalSupplies": i['mechanicalSupplies'],
                "repairMaintenance": i['repairMaintenance'],
                "meals": i['meals'],
                "transpo": i['transpo'],
                "tires": i['tires'],
                "amortization": i['amortization'],
                "others": i['others'],
                # "equipmentID": i['equipment_id']
            
            }
          for i in data
        ]
    

    return costData

@rizal_project.get("/api-test-costTable/")
async def test(username: str = Depends(validateLogin)):
    """This function is for testing"""

    data = selectCostAnalysis2()
    

    costData = [
        
            {
                "trans_date": i.trans_date,
                "equipment_id": i.equipment_id,
                "clasification":i.clasification,
                "cost_amount": i.cost_amount
                # "equipmentID": i['equipment_id']
            
            }
          for i in data
        ]


    return costData



#=======================================================Equipment Frame =================================================

@rizal_project.get("/rizal-eqipment/", response_class=HTMLResponse)
async def get_all_equipment(request: Request):
    
    return templates.TemplateResponse("rizal/equipment.html",{"request":request})

@rizal_project.get("/api-get-rizal-equipment/")
async def test(username: str = Depends(validateLogin)):
    """This function is for testing"""

    data = getEquipmentRizal()
    

    costData = [
        
            {
                "id": i.id,
                "equipment_id": i.equipment_id,
                "purchase_date":i.purchase_date,
                "description": i.description,
                "purchase_amount": i.purchase_amount,
                "rental_rate": i.rental_rate,
                "plate_number": i.plate_number,
                "status": i.status,
                "owner": i.owner,
            
            }
          for i in data
        ]


    return costData


@rizal_project.post("/api-insert-rizal-equipment/")
async def insertEquipment(items:EquipmentDetails,username: str = Depends(validateLogin)):
    """This function is to update employee Details"""
    insertEquipment(equipment_id=items.equipment_id,purchase_date=items.purchase_date,
                        description=items.description,purchase_amount=items.purchase_amount,
                        rental_rate=items.rental_rate,plate_number=items.plate_number,
                        status=items.status,owner=items.owner)


    return  {'Messeges':'Data has been Save'}   


@rizal_project.get("/update-equipment-rizal/{id}", response_class=HTMLResponse)
async def get_costData_id(id,request: Request):

    i = select_rizalEquipment_id(id=id)
    

    costData = [
        
            {
                "id": i.id,
                "equipment_id": i.equipment_id,
                "purchase_date":i.purchase_date,
                "description": i.description,
                "purchase_amount": i.purchase_amount,
                "rental_rate": i.rental_rate,
                "plate_number": i.plate_number,
                "status": i.status,
                "owner": i.owner
            
            }
           
        ]
    

    
    
    return templates.TemplateResponse("rizal/updateEquipment.html",{"request":request,"results":costData})


@rizal_project.put("/api-update-rizal-equipment/{id}")
async def updateRzEquipment(id,items:equipment_details,username: str = Depends(validateLogin)):

    """This function is for updating Rizal Equipment"""
    updateRizalequipment(equipment_id=items.equipment_id,purchase_date=items.purchase_date,
                        description=items.description,purchase_amount=items.purchase_amount,
                        rental_rate=items.rental_rate,plate_number=items.plate_number,
                        status=items.status,owner=items.owner,id=id)

    

    return  {'Messeges':'Data has been Updated'}


#==============================================Rizal Employee Credential ============================================

  