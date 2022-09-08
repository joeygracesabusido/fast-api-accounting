from fastapi import APIRouter, Body, HTTPException, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from config.db import mydb



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


@client.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    # user = mydb.login.find({"username":username})

    # for i in user:
    #     username = i['username']
    #     password = i['password']
    #     print(username, password)

    if authenticate_user(username, password):
        return {"access_token": username, "token_type": "bearer"}

    else :
        raise HTTPException(status_code=400, detail="Incorrect username or password")



#======================================Front End===================================================
@client.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request":request}) 

# @client.get("/login",response_class=HTMLResponse)
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#    username = form_data.username
#    password = form_data.password  




@client.get("/chart-of-account/", response_class=HTMLResponse)
async def index(request: Request, ):
    return templates.TemplateResponse("accounting_home.html", {"request":request})