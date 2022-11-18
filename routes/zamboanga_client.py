# import jwt
# from urllib import response
from fastapi import APIRouter, Body, HTTPException, Depends, Request, Response,status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from config.db import mydb


from bson import ObjectId
from typing import Optional

from datetime import timedelta, datetime

from schemas.chartofAccount import chartofAccount,chartofAccounts
from schemas.user import userEntity,usersEntity
from schemas.bstype import bsTypes
from schemas.journalEntry import journalEntry,journalEntrys,journalEntryZambo, journalEntryZambos
from schemas.journalEntry_incomeStatmement import journalEntry_incomeStatement,journalEntry_incomeStatements

from jose import jwt

JWT_SECRET = 'myjwtsecret'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

zamboanga_client = APIRouter(include_in_schema=False)


templates = Jinja2Templates(directory="templates")





def validateLogin(request:Request):
    """This function is for Log In Authentication"""
    
    try :
        token = request.cookies.get('access_token')
        # print(token)
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
            detail= "Not Authorized Please login",
            # headers={"WWW-Authenticate": "Basic"},
        )









@zamboanga_client.get("/view-journal-entry-zambo/", response_class=HTMLResponse)
async def view_journal_entry(request: Request):
    """This function is for displaying journal Entry"""
   
    myresult  = mydb.journal_entry_zambo.find()

    all_journalEntry = []
    for item in myresult:
        debit = item["debit_amount"]
        credit = item["credit_amount"]
        debit2 = '{:,.2f}'.format(debit)
        credit2 = '{:,.2f}'.format(credit)

        data = {}

        data.update({
            "id": item["_id"],
            "date_entry": item["date_entry"],
            "journal": item["journal"],
            "ref": item["ref"],
            "descriptions": item["descriptions"],
            "acoount_number": item["acoount_number"],
            "account_disc": item["account_disc"],
            "debit_amount": debit2,
            "credit_amount": credit2,
            "due_date_apv": item["due_date_apv"],
            "terms_days": item["terms_days"],
            "supplier/Client": item["supplier/Client"],
            "user": item["user"],
            "created": item["created"]

        })

        all_journalEntry.append(data)
    
    return templates.TemplateResponse("viewJournalEntry_zambo.html", {"request":request,
                                        "all_journalEntry":all_journalEntry})




@zamboanga_client.get("/insert-journal-entry-zambo/", response_class=HTMLResponse)
async def insert_journal_entry(request: Request):
    """This function is for openting navbar of accounting"""
    form = await request.form()
    accountTile = form.get('accountTitle')

   

    all_chart_of_account = chartofAccounts(mydb.chart_of_account.find().sort('accountTitle', 1))
    return templates.TemplateResponse("journal_entry_zamboanga.html", 
                                        {"request":request,"all_chart_of_account":all_chart_of_account})

@zamboanga_client.post("/insert-journal-entry-zambo/", response_class=HTMLResponse)
async def insert_journal_entry(request: Request):
    """This function is to post Journal Entry"""
    form = await request.form()

    trans_date = form.get('trans_date')
    journal = form.get('journal')
    reference = form.get('reference')
    journal_memo = form.get('journal_memo')
    accountTitle = form.get('accountTitle')
    debit_amount = form.get('debit_amount')
    credit_amount = form.get('credit_amount')

    date_time_obj_to = datetime.strptime(trans_date, '%Y-%m-%d')

    

    

    messeges = []
    
    try:

        token = request.cookies.get('access_token')

        all_journalEntry = ''
        if token is None:

            messeges.append("Please log in first to validated credentials ")
            return templates.TemplateResponse("journal_entry_zamboanga.html", 
                                                    {"request":request,'all_journalEntry':all_journalEntry,
                                                    "messeges":messeges})

            
        else:
            scheme, _, param = token.partition(" ")
            payload = jwt.decode(param, JWT_SECRET, algorithms=ALGORITHM)
        
            username = payload.get("sub")
        

            user =  mydb.login.find({"username":username})

            if user is not None:
                items = chartofAccounts(mydb.chart_of_account.find({'accountTitle':accountTitle}))
                for i in items:
                    accountNumber = i['accountNum']
                    bsType = i['bsClass']

                    dataInsert = {
                        # 'date_entry': journalEntryInsert_datefrom.get(),
                        'date_entry': date_time_obj_to,
                        'journal': journal,
                        'ref': reference,
                        'descriptions': journal_memo,
                        'acoount_number': accountNumber,
                        'account_disc': accountTitle,
                        'bsClass': bsType,
                        'debit_amount': float(debit_amount),
                        'credit_amount': float(credit_amount),
                        'due_date_apv': "",
                        'terms_days': "",
                        'supplier/Client': "",
                        'user': username,
                        'created':datetime.now()
                        
                        }

                    messeges.append("Entry Has been Save")
                    mydb.journal_entry_zambo.insert_one(dataInsert)

                    all_journalEntry  = journalEntryZambos(mydb.journal_entry_zambo.find({'ref':reference}))
                    
                    return templates.TemplateResponse("journal_entry_zamboanga.html", 
                                                    {"request":request,'all_journalEntry':all_journalEntry})
                    # return response.RedirectResponse(f'/insert-journal-entry-2/')
            messeges.append("Please log in first to validated credentials ")
            return templates.TemplateResponse("journal_entry_zamboanga.html", 
                                                    {"request":request,'all_journalEntry':all_journalEntry,
                                                   "messeges":messeges})

            
    
    except Exception as e:
        messeges.append(e)
        return templates.TemplateResponse("journal_entry_zamboanga.html", 
                                                {"request":request,'all_journalEntry':all_journalEntry,
                                                "messeges":messeges})

#=============================================This is need for debugging insert Journal Entry==================================
@zamboanga_client.get("/insert-journal-entry-zambo2/", response_class=HTMLResponse)
async def insert_journal_entry(request: Request):
    """This function is for openting navbar of accounting"""
    form = await request.form()
    accountTile = form.get('accountTitle')

   

    all_chart_of_account = chartofAccounts(mydb.chart_of_account.find().sort('accountTitle', 1))
    return templates.TemplateResponse("journal_entry_zamboanga2.html", 
                                        {"request":request,"all_chart_of_account":all_chart_of_account})


@zamboanga_client.post("/insert-journal-entry-zambo2/", response_class=HTMLResponse)
async def insert_journal_entry(request: Request):
    """This function is for posting accounting"""
    form = await request.form()

    trans_date = form.get('trans_date')
    journal = form.get('trasactionType')
    reference = form.get('reference')
    journal_memo = form.get('journal_memo')
    

    date_time_obj_to = datetime.strptime(trans_date, '%Y-%m-%d')

    
    account_title =[
        form.get('accountTitle1'),
        form.get('accountTitle2'),
        form.get('accountTitle3'),
        form.get('accountTitle4'),
        form.get('accountTitle5'),
        form.get('accountTitle6'),
        form.get('accountTitle7'),
        form.get('accountTitle8'),
        form.get('accountTitle9'),
        form.get('accountTitle10')
    ]

   
    

    debitAmount = [
        form.get('amount1'),
        form.get('amount2'),
        form.get('amount3'),
        form.get('amount4'),
        form.get('amount5'),
        form.get('amount6'),
        form.get('amount7'),
        form.get('amount8'),
        form.get('amount9'),
        form.get('amount10')
    ]
    

    craditAmount = [
        form.get('credit_amount1'),
        form.get('credit_amount2'),
        form.get('credit_amount3'),
        form.get('credit_amount4'),
        form.get('credit_amount5'),
        form.get('credit_amount6'),
        form.get('credit_amount7'),
        form.get('credit_amount8'),
        form.get('credit_amount9'),
        form.get('credit_amount10')

    ]

    

    res = []
    
    for val in account_title:
        if val != None :
            res.append(val)


    res2 = []
   
    for val in debitAmount:
        if val != None :
            res2.append(val)

    res3 = []
   
    for val in craditAmount:
        if val != None :
            res3.append(val)
            
   
    data= {}

    data.update({
        "accountTitle":res,
        "debit":res2,
        "credit":res3
    })

    entry = len(data['accountTitle'])
   

    result = []
    for i in range(entry):
        # print(i)
        d={}
        for j,k in enumerate(data.items()):
            if j == 0:
                d['accountTitle']= (k[1][i])

            if j == 1:
                d['debit']= (k[1][i])
               
            if j == 2:   
                d['credit']= (k[1][i])

        result.append(d)
    # print(result)
    
    totalD = 0
    totalC = 0
    accountTitle2 = ''
    debit2 = 0
    credit2 = 0
    totalAmount = 0
    messeges = []
    for r in result:
       
        
        accountTitle2 = r['accountTitle']
        debit2 = r['debit']
        credit2 = r['credit']
        totalD += float(debit2)
        totalC += float(credit2)
        total_debit = '{:.2f}'.format(totalD)
        total_credit = '{:.2f}'.format(totalC)

    totalAmount = float(total_debit)-float(total_credit)
    if totalAmount == 0:
   
        for r in result:
           
        
            accountTitle2 = r['accountTitle']
            debit2 = r['debit']
            credit2 = r['credit']
            totalD += float(debit2)
            totalC += float(credit2)

            try:

                token = request.cookies.get('access_token')

                all_chart_of_account = chartofAccounts(mydb.chart_of_account.find().sort('accountTitle', 1))
                if token is None:

                    messeges.append("Please log in first to validated credentials ")
                    return templates.TemplateResponse("journal_entry_zamboanga2.html", 
                                                            {"request":request,'all_chart_of_account':all_chart_of_account,
                                                            "messeges":messeges})

                    
                else:
                    scheme, _, param = token.partition(" ")
                    payload = jwt.decode(param, JWT_SECRET, algorithms=ALGORITHM)
                
                    username = payload.get("sub")
                

                    user =  mydb.login.find({"username":username})

                    if user is not None:
                        items = chartofAccounts(mydb.chart_of_account.find({'accountTitle':accountTitle2}))
                        for i in items:
                            accountNumber = i['accountNum']
                            bsType = i['bsClass']

                            

                            dataInsert = [{
                                
                                'date_entry': date_time_obj_to,
                                'journal': journal,
                                'ref': reference,
                                'descriptions': journal_memo,
                                'acoount_number': accountNumber,
                                'account_disc': accountTitle2,
                                'bsClass': bsType,
                                'debit_amount': float(debit2),
                                'credit_amount': float(credit2),
                                'due_date_apv': "",
                                'terms_days': "",
                                'supplier/Client': "",
                                'user': username,
                                'created':datetime.now()
                                
                                }]

                            
                                
                            # print(dataInsert)

                            
                            mydb.journal_entry_zambo.insert_many(dataInsert)

                    
            
            except Exception as e:
                messeges.append(e)
                return templates.TemplateResponse("journal_entry_zamboanga2.html", 
                                                        {"request":request,'all_chart_of_account':all_chart_of_account,
                                                        "messeges":messeges})
    else:
        messeges.append("Debit and Credit Not Balance")
        all_chart_of_account = chartofAccounts(mydb.chart_of_account.find().sort('accountTitle', 1))
        return templates.TemplateResponse("journal_entry_zamboanga2.html", 
                                            {"request":request,"all_chart_of_account":all_chart_of_account,
                                            "messeges":messeges})


    

    # data_ = form

    # listItems = (dict(data_._list))
    
    # listItems.pop('trans_date')
    # listItems.pop('trasactionType')
    # listItems.pop('reference')
    # listItems.pop('journal_memo')


    # print(listItems)
    # entry = len(listItems)
    # print(entry)

    # for k in listItems.items():
    #         print(k)

    # result =[]
    
    # d={}
    # for j,k in enumerate(listItems.items()):
    #     if j == 0:
    #         d['accountTitle']= (k[1])
    # result.append(d)
    
    # print(result)
        
   

    messeges.append("Data has been save")
    all_chart_of_account = chartofAccounts(mydb.chart_of_account.find().sort('accountTitle', 1))
    return templates.TemplateResponse("journal_entry.html", 
                                        {"request":request,"all_chart_of_account":all_chart_of_account,
                                        "messeges":messeges})






#=============================================This api for Income Statement Router========================
@zamboanga_client.get("/income-statement-zambo/", response_class=HTMLResponse)
async def get_income_statement(request:Request):
    """This function is for querying income statement"""
    return templates.TemplateResponse("incomestatement.html",{'request':request})

@zamboanga_client.post("/income-statement-zambo/", response_class=HTMLResponse)
async def get_income_statement(request:Request):
    """This function is for querying income statement"""
    form = await request.form()

    dateFrom = form.get('trans_date_from')
    date_time_obj_from = datetime.strptime(dateFrom, '%Y-%m-%d')

    dateTo = form.get('trans_date_to')
    date_time_obj_to = datetime.strptime(dateTo, '%Y-%m-%d')

    agg_result= mydb.journal_entry_zambo.aggregate(
        [
        {"$match":{'date_entry': {'$gte':date_time_obj_from, '$lte':date_time_obj_to},
            '$or': [
            {'acoount_number': {"$regex": "^5"}},
            {'acoount_number': {"$regex": "^4"}}
        ] }},
        # {"$match": { "cut_off_period": date } },
        # {'$sort' : { '$meta': "textScore" }, '$account_disc': -1 },
        {"$group" : 
            {"_id" :  '$acoount_number',
            "accountName": {'$first':'$account_disc'},
            "totalDebit" : {"$sum" : '$debit_amount'},
            "totalCredit" : {"$sum" : '$credit_amount'},
            
            }},
        {'$sort':{'_id': 1}}
            
        ])
    agg_result_list = []
    for x in agg_result:

        accountNumber = x['_id']
        account_title = x['accountName']
        debit_amount = x['totalDebit']
        debit_amount2 = '{:,.2f}'.format(debit_amount)
        credit_amount = x['totalCredit']
        credit_amount2 = '{:,.2f}'.format(credit_amount)
        totalIncome =   float(credit_amount) - float(debit_amount)
        totalIncome2 = '{:,.2f}'.format(totalIncome)

        

        data={}   
        
        data.update({
            
            
            'acoount_number': accountNumber,
            'accountTitle': account_title,
            'debit_amount': debit_amount2,
            'credit_amount': credit_amount2,
            'totalAmount': totalIncome2,
        })

        agg_result_list.append(data)


    

    return templates.TemplateResponse("incomestatement_zambo.html",{'request':request,'agg_result_list':agg_result_list})

#==================================================Trial Balance Frame =================================================
@zamboanga_client.get("/trialbalance-zambo/", response_class=HTMLResponse)
async def equipment_zamboanga(request:Request, username: str = Depends(validateLogin)):
    """This function is to show page for Trial Balance"""

    return templates.TemplateResponse("zamboanga/zamboangaTrialBal.html",{'request':request})


#==================================================Equipment Vitali =====================================================
@zamboanga_client.get("/zamboanga-equipment/", response_class=HTMLResponse)
async def equipment_zamboanga(request:Request, username: str = Depends(validateLogin)):
    """This function is to show page for Equipment"""

    user = username
    return templates.TemplateResponse("zamboanga/vitali_equipment.html",{'request':request,'user':user})

@zamboanga_client.get("/zamboanga-test-html/", response_class=HTMLResponse)
async def equipment_zamboanga(request:Request, username: str = Depends(validateLogin)):
    """This function is to show page for Equipment"""

    user = username
    return templates.TemplateResponse("zamboanga/test.html",{'request':request,'user':user})


