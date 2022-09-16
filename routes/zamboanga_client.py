# import jwt
# from urllib import response
from fastapi import APIRouter, Body, HTTPException, Depends, Request, Response
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




@zamboanga_client.get("/view-journal-entry-zambo/", response_class=HTMLResponse)
async def view_journal_entry(request: Request):
    """This function is for displaying journal Entry"""
   
    all_journalEntry  = journalEntryZambos(mydb.journal_entry_zambo.find())
    
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
        return templates.TemplateResponse("journal_entry2.html", 
                                                {"request":request,'all_journalEntry':all_journalEntry,
                                                "messeges":messeges})
#=============================================This ksi for Income Statement Router========================
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
    






