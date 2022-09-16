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
from schemas.journalEntry import journalEntry,journalEntrys
from schemas.journalEntry_incomeStatmement import journalEntry_incomeStatement,journalEntry_incomeStatements

from jose import jwt

JWT_SECRET = 'myjwtsecret'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

client = APIRouter(include_in_schema=False)


templates = Jinja2Templates(directory="templates")


#=======================================User JWT Token ===========================================
@client.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request":request})





from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

password1 = ""
def authenticate_user(username, password):
    
    user = mydb.login.find({"username":username})

    for i in user:
        username = i['username']
        password1 = i['password']
   
        if user:
            
            password_check = pwd_context.verify(password,password1)
            
            return password_check

            
        else :
            False

@client.post('/login2')
def cookie(response: Response):
    response.set_cookie(key="mysession", value="1242r")
    return {"message": "Wanna cookie?"}

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()

    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})

    
    return to_encode

    # print(to_encode)

    # token = jwt.encode(to_encode, JWT_SECRET,algorithm=ALGORITHM)
    #         # print(token)
    # msg ='Login Succesful'
    # response = templates.TemplateResponse("login.html", {"request":request,"msg":msg})
    # response.set_cookie(key="access_token", value=f'Bearer {token}',httponly=True)
    # return response



@client.post('/login')
# def login(request: Request,response: Response,form_data: OAuth2PasswordRequestForm = Depends()):
async def login(response: Response, request:Request):
    form =  await request.form()
    username = form.get('username')
    password = form.get('password')

    # username = form_data.username
    # password = form_data.password

    
    
    errors =[]
    msg = []
    try:
        if authenticate_user(username, password):
            access_token = create_access_token(
                data = {"sub": username}, 
                expires_delta=timedelta(minutes=30)
                                    )
            # data = create_access_token
            # data = {"sub":username}
            

            # data={}
            # user =  mydb.login.find({"username":username})

            # for i in user:
            #     idNum = i['_id']
            #     username1 = i['username']
            #     password1 = i['password']
            
            #     data.update({
            #         'username': username1,
            #         'password': password1,
                    
            #     })
            
            
            token = jwt.encode(access_token, JWT_SECRET,algorithm=ALGORITHM)
            
            msg.append('Login Succesful')
            response = templates.TemplateResponse("login.html", {"request":request,"msg":msg})
            response.set_cookie(key="access_token", value=f'Bearer {token}',httponly=True)
            return response
            
           

        else :
            raise HTTPException(status_code=400, detail="Incorrect username or password")
    except:
        errors.append('Something wrong')
        return templates.TemplateResponse("login.html", {"request":request,"msg":msg})


#======================================Front End===================================================
@client.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request":request}) 

# @client.get("/login",response_class=HTMLResponse)
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#    username = form_data.username
#    password = form_data.password  




@client.get("/chart-of-account/", response_class=HTMLResponse)
def chart_of_account_view(request: Request):
    """This function is for openting navbar of accounting"""
    all_chart_of_account = chartofAccounts(mydb.chart_of_account.find().sort('accountNum', 1))
    all_bstype = bsTypes(mydb.balansheetType.find())
    return templates.TemplateResponse("accounting_home.html", {"request":request,
                                            "all_chart_of_account":all_chart_of_account,
                                            "all_bstype":all_bstype})


   
        
@client.post("/chart-of-account/", response_class=HTMLResponse)
async def insert_chart_of_account(request: Request):
    """This function is for inserting Chart of account"""
    form =  await request.form()
    account_number = form.get('account_number')
    account_title = form.get('account_title')
    bstype = form.get('bstype')

    messeges = []
    
    query = {'accountNum':account_number}
                   
    agg_result= mydb.chart_of_account.count_documents(query)

    all_chart_of_account = chartofAccounts(mydb.chart_of_account.find().sort('accountNum', 1))
    all_bstype = bsTypes(mydb.balansheetType.find())

    if agg_result > 0:
        messeges.append("Account Number already Taken")
        return templates.TemplateResponse("accounting_home.html", {"request":request,
                                                    "all_chart_of_account":all_chart_of_account,
                                                    "all_bstype":all_bstype,"messeges":messeges})

    else:
        try:
            token = request.cookies.get('access_token')
        # print(token)

            if token is None:

                messeges.append("Please Log in to Transact")
                return templates.TemplateResponse("accounting_home.html", {"request":request,
                                                                    "all_chart_of_account":all_chart_of_account,
                                                                    "all_bstype":all_bstype,"messeges":messeges})

                
            else:
                scheme, _, param = token.partition(" ")
                payload = jwt.decode(param, JWT_SECRET, algorithms=ALGORITHM)
            
                username = payload.get("sub")
            

                user =  mydb.login.find({"username":username})

                if user is not None:

                    dataInsert = {
                        'accountNum': account_number,
                        'accountTitle': account_title,
                        'bsClass': bstype,
                        'user': username,
                        'created': datetime.now()
                        
                        }

                    mydb.chart_of_account.insert_one(dataInsert)

                    messeges.append("Your Account Title has been Save")
                    return templates.TemplateResponse("accounting_home.html", {"request":request,
                                                                "all_chart_of_account":all_chart_of_account,
                                                                "all_bstype":all_bstype,"messeges":messeges})
            
        except Exception as e:
            messeges.append(e)
            return templates.TemplateResponse("accounting_home.html", {"request":request,
                                                                "all_chart_of_account":all_chart_of_account,
                                                                "all_bstype":all_bstype,"messeges":messeges})

@client.get("/update-chart-of-account/{id}", response_class=HTMLResponse)
def update_chart_of_account(id,request: Request):
    """This function is for showing Form for Updating Chart of Account"""
    token = request.cookies.get('access_token')
    
    search_coa = chartofAccounts(mydb.chart_of_account.find({"_id":ObjectId(id)}))
    
    return templates.TemplateResponse("update_coa.html", {"request":request,'search_coa':search_coa})


@client.post("/update-chart-of-account/{id}", response_class=HTMLResponse)
async def update_chart_of_account(id,request: Request):
    """This function is for inserting Chart of account"""
    form =  await request.form()
    account_number = form.get('account_number')
    account_title = form.get('account_title')
    bstype = form.get('bsClass')
    user_search = form.get('user')

    messeges = []

    try:
     
        token = request.cookies.get('access_token')
        if token is None:

            messeges.append("Please Log in to Transact")
            search_coa = chartofAccounts(mydb.chart_of_account.find({"_id":ObjectId(id)}))
    
            return templates.TemplateResponse("update_coa.html", {"request":request,'search_coa':search_coa,
                                                'messeges':messeges})
            
        else:
            scheme, _, param = token.partition(" ")
            payload = jwt.decode(param, JWT_SECRET, algorithms=ALGORITHM)
        
            username = payload.get("sub")
        

            user =  mydb.login.find({"username":username})

            if user is not None:

                query = {'_id':ObjectId(id)}

                newValue = { "$set": {  
                                            
                                            'accountTitle': account_title,
                                            'bsClass': bstype,
                                            'user': user_search,
                                            'created': datetime.now()
                                            
                                        }           
                                    }


                mydb.chart_of_account.update_one(query, newValue)

                messeges.append("Your Account Title has been Save")
                all_chart_of_account = chartofAccounts(mydb.chart_of_account.find().sort('accountNum', 1))
                all_bstype = bsTypes(mydb.balansheetType.find())
                return templates.TemplateResponse("accounting_home.html", {"request":request,
                                                            "all_chart_of_account":all_chart_of_account,
                                                            "messeges":messeges})

        
        
    except Exception as e:
        messeges.append(e)
        return templates.TemplateResponse("accounting_home.html", {"request":request,
                                                            "all_chart_of_account":all_chart_of_account,
                                                            "all_bstype":all_bstype,"messeges":messeges})

@client.get("/view-journal-entry/", response_class=HTMLResponse)
async def view_journal_entry(request: Request):
    """This function is for displaying journal Entry"""
   
    all_journalEntry  = journalEntrys(mydb.journal_entry.find())
    
    return templates.TemplateResponse("viewJournalEntry.html", {"request":request,"all_journalEntry":all_journalEntry})


@client.get("/autocomplete/")
def autocomplete(term: Optional[str]):
    items = chartofAccounts(mydb.chart_of_account.find({'accountTitle':{"$regex":term,'$options':'i'}}))

    suggestions = []
    for item in items:
        suggestions.append(item['accountTitle'])
    return suggestions

@client.get("/insert-journal-entry-2/", response_class=HTMLResponse)
async def insert_journal_entry(request: Request):
    """This function is for openting navbar of accounting"""
    form = await request.form()
    accountTile = form.get('accountTitle')

   

    all_chart_of_account = chartofAccounts(mydb.chart_of_account.find().sort('accountTitle', 1))
    return templates.TemplateResponse("journal_entry2.html", 
                                        {"request":request,"all_chart_of_account":all_chart_of_account})

@client.post("/insert-journal-entry-2/", response_class=HTMLResponse)
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
            return templates.TemplateResponse("journal_entry2.html", 
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
                    mydb.journal_entry.insert_one(dataInsert)

                    all_journalEntry  = journalEntrys(mydb.journal_entry.find({'ref':reference}))
                    
                    return templates.TemplateResponse("journal_entry2.html", 
                                                    {"request":request,'all_journalEntry':all_journalEntry})
                    # return response.RedirectResponse(f'/insert-journal-entry-2/')
            messeges.append("Please log in first to validated credentials ")
            return templates.TemplateResponse("journal_entry2.html", 
                                                    {"request":request,'all_journalEntry':all_journalEntry,
                                                   "messeges":messeges})

            
    
    except Exception as e:
        messeges.append(e)
        return templates.TemplateResponse("journal_entry2.html", 
                                                {"request":request,'all_journalEntry':all_journalEntry,
                                                "messeges":messeges})
#=============================================This ksi for Income Statement Router========================
@client.get("/income-statement/", response_class=HTMLResponse)
async def get_income_statement(request:Request):
    """This function is for querying income statement"""
    return templates.TemplateResponse("incomestatement.html",{'request':request})

@client.post("/income-statement/", response_class=HTMLResponse)
async def get_income_statement(request:Request):
    """This function is for querying income statement"""
    form = await request.form()

    dateFrom = form.get('trans_date_from')
    date_time_obj_from = datetime.strptime(dateFrom, '%Y-%m-%d')

    dateTo = form.get('trans_date_to')
    date_time_obj_to = datetime.strptime(dateTo, '%Y-%m-%d')

    agg_result= mydb.journal_entry.aggregate(
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


    

    return templates.TemplateResponse("incomestatement.html",{'request':request,'agg_result_list':agg_result_list})
    

#=============================================This is need for debugging==================================
@client.get("/insert-journal-entry/", response_class=HTMLResponse)
async def insert_journal_entry(request: Request):
    """This function is for openting navbar of accounting"""
    form = await request.form()
    accountTile = form.get('accountTitle')

   

    all_chart_of_account = chartofAccounts(mydb.chart_of_account.find().sort('accountTitle', 1))
    return templates.TemplateResponse("journal_entry.html", 
                                        {"request":request,"all_chart_of_account":all_chart_of_account})


@client.post("/insert-journal-entry/", response_class=HTMLResponse)
async def insert_journal_entry(request: Request):
    """This function is for posting accounting"""
    form = await request.form()
    accountTile = form.get('accountTitle')

    
    
    data_ = form

    print(data_)
    # data_.pop('BalanceSheetType')
    # data_.pop('reference')
    # data_.pop('journal_memo')
    # data_.pop('submit')
    
    # print(entry)

    # for i in range(entry):
    #     result = []
    #     d={}
    #     for j,k in enumerate(data_.items()):

    #         if j == 8:
    #             d['accountTitle']= (k[8][i])
    #         result.append(d)
    #     print(result)

    all_chart_of_account = chartofAccounts(mydb.chart_of_account.find().sort('accountTitle', 1))
    return templates.TemplateResponse("journal_entry.html", 
                                        {"request":request,"all_chart_of_account":all_chart_of_account})




