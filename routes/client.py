# import jwt
# from urllib import response
from distutils.command.config import config
from traceback import format_list
from typing import Union, List
from fastapi import APIRouter, Body, HTTPException, Depends, Request, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
# from config.db import mydb

from config.mongodb_con import create_mongo_client
mydb = create_mongo_client()
# from config.db import create_mongo_client

# mydb = create_mongo_client()
# from config.db import worker


from bson import ObjectId
from typing import Optional

from datetime import timedelta, datetime,date

from models.model import User

from schemas.chartofAccount import chartofAccount,chartofAccounts
from schemas.user import userEntity,usersEntity
from schemas.bstype import bsTypes
from schemas.journalEntry import journalEntry,journalEntrys
from schemas.journalEntry_incomeStatmement import journalEntry_incomeStatement,journalEntry_incomeStatements

from starlette.responses import PlainTextResponse

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
    
    user = mydb.login.find({'$and':[{"username":username},{'status':'approved'}]})

    for i in user:
        username = i['username']
        password1 = i['password']
   
        if user:
            
            password_check = pwd_context.verify(password,password1)
            
            return password_check

            
        else :
            False



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

@client.get("/favicon.ico")
async def disable_favicon():
    return PlainTextResponse("Favicon not found", status_code=404)


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
            msg.append('Incorrect username or password or you are Not Approved Yet')
            # raise HTTPException(status_code=400, detail="Incorrect username or password")
            return templates.TemplateResponse("login.html", {"request":request,"msg":msg})
    except:
        errors.append('Something wrong')
        return templates.TemplateResponse("login.html", {"request":request,"msg":msg})
        

def SurigaovalidateLogin(request:Request):
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
            detail= "Not Authorized Please login",
            # headers={"WWW-Authenticate": "Basic"},
        )


@client.post('/sign-up-admin')
def sign_up(items:User):
    """This function is for inserting """
    dataInsert = dict()
    dataInsert = {
        "fullname": items.fullname,
        "username": items.username,
        "password": get_password_hash(items.password),
        "status": items.status,
        "created": items.created
        
        }
    mydb.login.insert_one(dataInsert)
    return {"message":"User has been save"} 


@client.put('/api-update-admin-user/')
async def update_employee_status(id,status:Optional[str], username = Depends(SurigaovalidateLogin)):
    """This function is to update user info"""
    mydb.login.find_one_and_update({"_id":ObjectId(id)},{
        "$set":{
            "status":status
        }
    })
    return {'Messaeges':'Data has been updated'}

@client.get('/api-get-admin-user/')
async def get_employee_user(fullname, username = Depends(SurigaovalidateLogin)):
    """This is for search of employee"""
    return  usersEntity(mydb.login.find({'fullname':{"$regex":fullname,'$options':'i'}}))

@client.get("/api-autocomplete-admin-user/")
def autocomplete(term: Optional[str], username = Depends(SurigaovalidateLogin)):
    """this is for auto complete of """
    items = usersEntity(mydb.login.find({'fullname':{"$regex":term,'$options':'i'}}))

    suggestions = []
    for item in items:
        suggestions.append(item['fullname'])
    return suggestions




#======================================Front End===================================================
@client.get("/login", response_class=HTMLResponse)
async def login_show(request: Request):
    return templates.TemplateResponse("login.html", {"request":request}) 

# @client.get("/login",response_class=HTMLResponse)
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#    username = form_data.username
#    password = form_data.password  




@client.get("/chart-of-account/", response_class=HTMLResponse)
def chart_of_account_view(request: Request,username: str = Depends(SurigaovalidateLogin)):
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
def update_chart_of_account(id,request: Request,username: str = Depends(SurigaovalidateLogin)):
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
                                            'accountNum':account_number,
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
async def view_journal_entry(request: Request,username: str = Depends(SurigaovalidateLogin)):
    """This function is for displaying journal Entry"""
   
    myresult  = mydb.journal_entry.find()

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
        
    
    return templates.TemplateResponse("viewJournalEntry.html", {"request":request,"all_journalEntry":all_journalEntry})


@client.get("/autocomplete/")
def autocomplete(term: Optional[str]):
    items = chartofAccounts(mydb.chart_of_account.find({'accountTitle':{"$regex":term,'$options':'i'}}))

    suggestions = []
    for item in items:
        suggestions.append(item['accountTitle'])
    return suggestions

@client.get("/insert-journal-entry-2/", response_class=HTMLResponse)
async def insert_journal_entry(request: Request,username: str = Depends(SurigaovalidateLogin)):
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
async def get_income_statement(request:Request,username: str = Depends(SurigaovalidateLogin)):
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
            "bsClass": {'$first':'$bsClass'},
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
        bsClass = x['bsClass']

        

        data={}   
        
        data.update({
            'acoount_number': accountNumber,
            'accountTitle': account_title,
            'debit_amount': debit_amount2,
            'credit_amount': credit_amount2,
            'totalAmount': totalIncome2,
            'bsClass': bsClass
        })

        agg_result_list.append(data)


    

    return templates.TemplateResponse("incomestatement.html",{'request':request,'agg_result_list':agg_result_list})


#===========================================Trial Balance Transactions=============================================
@client.get("/trialbalance-surigao/", response_class=HTMLResponse)
async def equipment_zamboanga(request:Request, username: str = Depends(SurigaovalidateLogin)):
    """This function is to show page for Trial Balance"""

    return templates.TemplateResponse("surigao/surigaoTrialBal.html",{'request':request})
    

#=============================================This is need for debugging insert Journal Entry==================================
@client.get("/insert-journal-entry/", response_class=HTMLResponse)
async def insert_journal_entry(request: Request, username: str = Depends(SurigaovalidateLogin)):
    """This function is for openting navbar of accounting"""
    form = await request.form()
    accountTile = form.get('accountTitle')

   

    all_chart_of_account = chartofAccounts(mydb.chart_of_account.find().sort('accountTitle', 1))
    return templates.TemplateResponse("journal_entry.html", 
                                        {"request":request,"all_chart_of_account":all_chart_of_account})


@client.post("/insert-journal-entry/", response_class=HTMLResponse)
async def insert_journal_entry(request: Request,username: str = Depends(SurigaovalidateLogin)):
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
        form.get('accountTitle10'),
        form.get('accountTitle11'),
        form.get('accountTitle12')
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
        form.get('amount10'),
        form.get('amount11'),
        form.get('amount12')
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
        form.get('credit_amount10'),
        form.get('credit_amount11'),
        form.get('credit_amount12')

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
                    return templates.TemplateResponse("journal_entry.html", 
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

                            
                            mydb.journal_entry.insert_many(dataInsert)

                    
            
            except Exception as e:
                messeges.append(e)
                return templates.TemplateResponse("journal_entry.html", 
                                                        {"request":request,'all_chart_of_account':all_chart_of_account,
                                                        "messeges":messeges})
    else:
        messeges.append("Debit and Credit Not Balance")
        all_chart_of_account = chartofAccounts(mydb.chart_of_account.find().sort('accountTitle', 1))
        return templates.TemplateResponse("journal_entry.html", 
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
# =========================================Updating Journal Entry ====================================

@client.get('/update-journal-entry-sur/{id}',response_class=HTMLResponse)
async def update_journalEntry_sur(id,request:Request, username: str = Depends(SurigaovalidateLogin)):
    """This function is for updating Journal Entry"""
    username1 = username
    search_journalEntry = mydb.journal_entry.find({"_id":ObjectId(id)})

    agg_result_list = []
    for i in search_journalEntry:
        transID = i['_id']
        trans_date = i['date_entry']
        journal = i['journal']
        reference = i['ref']
        journal_memo =i['descriptions']
        accountNumber = i['acoount_number']  
        accountTitle2 = i['account_disc']
        bsType = i['bsClass']
        debit2 = i['debit_amount']
        credit2 = i['credit_amount']
        # date_time_obj_to = datetime.strptime(trans_date, '%Y-%m-%d %H-%M-%S')
        
        

        data={}   
        
        data.update({
            'transID': transID,
            'date_entry': trans_date,
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
            'user': username1,
            'created':datetime.now()
        })

        agg_result_list.append(data)
        
        

    return templates.TemplateResponse('surigao/updateJournal_entry_sur.html',{'request':request,
                                        'user':username1,'journaEntry':agg_result_list})

from models.model import UpdateJVEntry_surigao
@client.put('/api-update-journal-entry-sur/{id}')
async def update_bstype(id,item:UpdateJVEntry_surigao):
    """This function is to update user info"""
    mydb.journal_entry.find_one_and_update({"_id":ObjectId(id)},{
        "$set":dict(item)
    })
    return {"Messeges":"Data Has been Updated"}

@client.get('/api-search-chart-account-sur/')
async def search_chartofAccount(accountTitle2):
    items = mydb.chart_of_account.find({'accountTitle':accountTitle2})

    agg_result_list = []
    for i in items:
        accountNumber = i['accountNum']
        bsType = i['bsClass']

        data={}   
        
        data.update({
            'accountNumber': accountNumber,
            'bsType': bsType,
             
        })

        agg_result_list.append(data)
    return agg_result_list

#========================================Surigao MYSQL DATA Base=======================================
from config.surigaoDB import SurigaoDB
SurigaoDB.initialize()


@client.get("/dollar-bill/", response_class=HTMLResponse)
def get_dollarBill_records(request: Request,username: str = Depends(SurigaovalidateLogin)):
    """This function is for querying diesel consuption from Rizal Project"""
   
    myresult = SurigaoDB.select_all_from_dollarBill()
   

    agg_result_list = []
    for x in myresult:
        id = x[0]
        trans_date = x[1]
        equipment_id = x[2]
        trackFactor = x[3]
        no_trips = x[4]
        totalVolume = x[5]
        usd_pmt = x[6]
        usd_totalAmount = x[7]
        convertion_rate = x[8]
        php_amount = x[9]
        vat_output = x[11]
        net_of_vat = x[12]
        usd_pmt2 = '{:,.2f}'.format(usd_pmt)
        usd_totalAmount2 = '{:,.2f}'.format(usd_totalAmount)
        php_amount2 = '{:,.2f}'.format(php_amount)
        vat_output2 = '{:,.2f}'.format(vat_output)
        net_of_vat2 = '{:,.2f}'.format(net_of_vat)
        

        data={}   
        
        data.update({
            'id': id,
            'trans_date': trans_date,
            'equipment_id': equipment_id,
            'trackFactor': trackFactor,
            'no_trips': no_trips,
            'totalVolume': totalVolume,
            'usd_pmt': usd_pmt2,
            'usd_totalAmount': usd_totalAmount2,
            'convertion_rate': convertion_rate,
            'php_amount': php_amount2,
            'vat_output': vat_output2,
            'net_of_vat': net_of_vat2,
        })

        agg_result_list.append(data)

    equipmentResult = SurigaoDB.select_all_equipment()
   

    agg_result_list_eqp = []
    for x in equipmentResult:
        id_eqp = x[0]
        equipment_id = x[1]

        data={}   
        
        data.update({
            'id': id_eqp,
            'equipment_id': equipment_id,
            
        })

        agg_result_list_eqp.append(data)

    # tax_value = [['Vat','Non-Vat'],[.12 ,1]]

    # val_result=[]
    # data={}   
    
    # data.update({
    #     'val_text': tax_value[0],
    #     'val':tax_value[1]
        
    # })
    # val_result.append(data)

    # print(val_result)
    
    return  templates.TemplateResponse("dollar_bill.html", 
                                        {"request":request,"agg_result_list":agg_result_list,
                                        "agg_result_list_eqp":agg_result_list_eqp
                                        })


@client.post("/dollar-bill/", response_class=HTMLResponse)
async def insert_dollarBill(request: Request, username: str = Depends(SurigaovalidateLogin)):
    """This function is to insert Data to dollar Bill Table"""
    form = await request.form()

    trans_date = form.get('trans_date')
    equipment_id = form.get('equipment_id')
    no_trips = form.get('no_trips')
    trackFactor = form.get('trackFactor')
    usd_pmt = form.get('usd_pmt')
    convertion_rate = form.get('convertion_rate')
    taxRate = form.get('taxRate')
    vat_output = form.get('vat_output')
    
    date_credited = date.today()
   
    username = username

   
    try:

        SurigaoDB.insert_production(trans_date=trans_date,equipment_id=equipment_id,trackFactor=trackFactor,
                                no_trips=no_trips,usd_pmt=usd_pmt,convertion_rate=convertion_rate,taxRate=taxRate,
                                vat_output=vat_output,date_credited=date_credited)

        myresult = SurigaoDB.select_all_from_dollarBill()
   

        agg_result_list = []
        for x in myresult:
            id = x[0]
            trans_date = x[1]
            equipment_id = x[2]
            trackFactor = x[3]
            no_trips = x[4]
            totalVolume = x[5]
            usd_pmt = x[6]
            usd_totalAmount = x[7]
            convertion_rate = x[8]
            php_amount = x[9]
            usd_pmt2 = '{:,.2f}'.format(usd_pmt)
            usd_totalAmount2 = '{:,.2f}'.format(usd_totalAmount)
            php_amount2 = '{:,.2f}'.format(php_amount)
        
            
            

            data={}   
            
            data.update({
                'id': id,
                'trans_date': trans_date,
                'equipment_id': equipment_id,
                'trackFactor': trackFactor,
                'no_trips': no_trips,
                'totalVolume': totalVolume,
                'usd_pmt': usd_pmt2,
                'usd_totalAmount': usd_totalAmount2,
                'convertion_rate': convertion_rate,
                'php_amount': php_amount2,
            })

            agg_result_list.append(data)

            return  templates.TemplateResponse("dollar_bill.html", 
                                        {"request":request,
                                        "agg_result_list":agg_result_list})

    except Exception as e:
        print(e)

    return  templates.TemplateResponse("dollar_bill.html", 
                                        {"request":request,
                                        "username":username})


@client.get("/update-dollar-bill/{id}", response_class=HTMLResponse)
async def update_dollarBill(id,request: Request, username: str = Depends(SurigaovalidateLogin)):
    """This function is for Updating Dollar Bill"""

    


    myresult = SurigaoDB.select_one_from_dollarBill(id=id)
   
    
    agg_result_list = []
    

    id_update = myresult[0]
    trans_date = myresult[1]
    equipment_id = myresult[2]
    trackFactor = myresult[3]
    no_trips = myresult[4]
    usd_pmt = myresult[6]
    convertion_rate = myresult[8]
    taxRate = myresult[10]
    vat_output = myresult[11]

    username = username
    
    data={}   
    
    data.update({
        'trans_id': id_update,
        'trans_date': trans_date,
        'equipment_id2': equipment_id,
        'trackFactor': trackFactor,
        'no_trips': no_trips,
        'usd_pmt': usd_pmt,
        'convertion_rate': convertion_rate,
        'taxRate': taxRate,
        'vat_output': vat_output,
       
    })

    agg_result_list.append(data)


    return templates.TemplateResponse("dollar_bill_update.html",{"request":request,
                                            "agg_result_list":agg_result_list,
                                            "username":username})

from config.surigaoDB import SurigaoDB
SurigaoDB.initialize()
@client.get("/peso-bill/", response_class=HTMLResponse)
def get_peso_records(request: Request,username: str = Depends(SurigaovalidateLogin)):
    """This function is for showing Page for Peso Biling Surigao Project"""

    user = username

    equipmentResult = SurigaoDB.select_all_equipment()
   

    agg_result_list_eqp = []
    for x in equipmentResult:
        id_eqp = x[0]
        equipment_id = x[1]

        data={}   
        
        data.update({
            'id': id_eqp,
            'equipment_id': equipment_id,
            
        })

        agg_result_list_eqp.append(data)

    result = SurigaoDB.select_all_from_peso()
   

    agg_result_list = []
    for x in result:
        id_ = x[0]
        transdate = x[1]
        equipment_id = x[2]
        ore_owner = x[3]
        trackFactor = x[4]
        no_trips = x[5]
        distance = x[6]
        totalVolume = x[7]
        rate = x[8]
        php_amount = x[9]
        taxRate = x[10]
        vat_output = x[11]
        net_of_vat = x[12]


        data={}   
        
        data.update({
            'id': id_,
            'transdate': transdate,
            'equipment_id': equipment_id,
            'ore_owner': ore_owner,
            'trackFactor': trackFactor,
            'no_trips': no_trips,
            'distance': distance,
            'totalVolume': totalVolume,
            'rate': rate,
            'php_amount': php_amount,
            'taxRate': taxRate,
            'vat_output': vat_output,
            'net_of_vat': net_of_vat,
            
        })

        agg_result_list.append(data)

    


    return  templates.TemplateResponse("surigao_pesoBill.html", 
                                    {"request":request,"agg_result_list_eqp":agg_result_list_eqp,
                                    "agg_result_list":agg_result_list,"user":user})

@client.get("/update-peso-bill/{id}", response_class=HTMLResponse)
async def update_pesoBill(id,request: Request,username: str = Depends(SurigaovalidateLogin)):
    """This function is for Updating Dollar Bill"""

    myresult = SurigaoDB.select_one_from_pesoBill(id=id)
   
    
    agg_result_list = []
    

    id_update = myresult[0]
    trans_date = myresult[1]
    equipment_id = myresult[2]
    ore_owner = myresult[3]
    trackFactor = myresult[4]
    no_trips = myresult[5]
    distance = myresult[6]
    rate = myresult[8]
    taxRate = myresult[10]
    vat_output = myresult[11]

    user = username
    
    data={}   
    
    data.update({
        'trans_id': id_update,
        'trans_date': trans_date,
        'equipment_id': equipment_id,
        'ore_owner': ore_owner,
        'trackFactor': trackFactor,
        'no_trips': no_trips,
        'distance': distance,
        'rate': rate,
        'taxRate': taxRate,
        'vat_output': vat_output,
       
    })

    agg_result_list.append(data)


    return templates.TemplateResponse("surigao_pesoBill_update.html",{"request":request,
                                            "agg_result_list":agg_result_list,"user":user
                                            })



