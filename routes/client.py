import jwt
# from urllib import response
from fastapi import APIRouter, Body, HTTPException, Depends, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from config.db import mydb

from schemas.chartofAccount import chartofAccount,chartofAccounts
from schemas.user import userEntity,usersEntity

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
            data = {"sub":username}

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
            
                
            token = jwt.encode(data, JWT_SECRET,algorithm=ALGORITHM)
            # print(token)
            msg.append('Login Succesful')
            response = templates.TemplateResponse("login.html", {"request":request,"msg":msg})
            response.set_cookie(key="access_token", value=f'Bearer {token}',httponly=True)
            return response
            
            # msg.append('Login Succesful')
            # return templates.TemplateResponse("login.html", {"request":request,"msg":msg})

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
def index(request: Request):
    # response.set_cookie(key="access_token",value=f'Bearer {password1}',HttpOnly=True)
    token = request.cookies.get('access_token')
    # print(token)

    if token:
        scheme, _, param = token.partition(" ")
        payload = jwt.decode(param, JWT_SECRET, algorithms=ALGORITHM)
       
        username = payload.get("sub")
       

        user =  mydb.login.find({"username":username})

        if user is not None:
            all_chart_of_account = chartofAccounts(mydb.chart_of_account.find().sort('accountNum', 1))
            return templates.TemplateResponse("accounting_home.html", {"request":request,
                                                    "all_chart_of_account":all_chart_of_account})
        else:
            return {"Details":"Kindly Login"}
        
        # return templates.TemplateResponse("login.html", {"request":request})
        
   