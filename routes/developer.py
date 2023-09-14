
from authentication.utils import OAuth2PasswordBearerWithCookie

from fastapi import APIRouter, Body, HTTPException, Depends, Request, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Union, List
from datetime import datetime

from bson import ObjectId
from typing import Optional


from datetime import timedelta, datetime,date




from schemas.user import usersEntity


from config.db import mydb





from jose import jwt

JWT_SECRET = 'myjwtsecret'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

developer = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")



from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")



from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

password1 = ""
def authenticate_user(username:str, password:str):
    
    result = mydb.developer_credential.find({'$and':[{"username":username},{'status':'Approved'}]})
    

    user = next((user for user in result if user["username"] == username), None)
    
    if user and pwd_context.verify(password, user["password"]):
        
        return user



def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()

    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})

    
    return to_encode

  



@developer.get('/api-developer-login/')
async def login(response: Response, request:Request):
    form =  await request.form()
    username = form.get('username')
    password = form.get('password')

    # username = username
    # password = password

    
    
    errors =[]
    msg = []
    try:
        if authenticate_user(username, password):
            access_token = create_access_token(
                data = {"sub": username}, 
                expires_delta=timedelta(minutes=30)
                                    )
          
            
            
            token = jwt.encode(access_token, JWT_SECRET,algorithm=ALGORITHM)
            print(token)
            msg.append('Login Succesful')
            response = RedirectResponse(url="/developer-transaction")
            response.set_cookie(key="access_token", value=f'Bearer {token}',httponly=True)
            # return templates.TemplateResponse("developer/transaction.html")
            
            return response

        
        else :
            msg.append('Incorrect username or password')
            # raise HTTPException(status_code=400, detail="Incorrect username or password")
            return templates.TemplateResponse("developer/transaction.html", {"request":request,"msg":msg})
    except:
        errors.append('Something wrong')
        return templates.TemplateResponse("developer/login.html", {"request":request,"msg":msg})

#======================================Login for Front End or API Login=============================
@developer.get("/developer-login/", response_class=HTMLResponse)
async def api_login(request: Request):
    return templates.TemplateResponse("developer/login.html", {"request":request}) 

def developer_Login(request:Request):
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
            detail= "Not Authorized Please login",)
            # headers={"WWW-Authenticate": "Basic"},

@developer.get("/developer-transaction/", response_class=HTMLResponse)
async def developer_login(request: Request):
    return templates.TemplateResponse("developer/transaction.html", {"request":request}) 
