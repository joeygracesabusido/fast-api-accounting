
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


from config.mongodb_con import create_mongo_client
mydb = create_mongo_client()
# from config.db import mydb
# from config.db import create_mongo_client
# mydb = create_mongo_client()

from models.model import AccessSetting





from jose import jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
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


def authenticate_user(username:str, password:str):
    
    result = mydb.developer_credential.find({'$and':[{"username":username},{'status':'Approved'}]})
    

    user = next((user for user in result if user["username"] == username), None)
    
    try:
        if user and pwd_context.verify(password, user["password"]):
            
            return user


    except Exception as ex:
        error_message = f"Error due to: {str(ex)}"
        print(error_message)
        return {"error": error_message}

    



def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()

    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})

    
    return to_encode

  



# @developer.get('/api-developer-login/')
# async def login(response: Response, request:Request):
#     form =  await request.form()
#     username = form.get('username')
#     password = form.get('password')

#     # username = username
#     # password = password

    
    
#     errors =[]
#     msg = []
#     try:
#         if authenticate_user(username, password):
#             access_token = create_access_token(
#                 data = {"sub": username}, 
#                 expires_delta=timedelta(minutes=30)
#                                     )
          
            
            
#             token = jwt.encode(access_token, JWT_SECRET,algorithm=ALGORITHM)
#             print(token)
#             msg.append('Login Succesful')
#             response = RedirectResponse(url="/developer-transaction")
#             response.set_cookie(key="access_token", value=f'Bearer {token}',httponly=True)
#             # return templates.TemplateResponse("developer/transaction.html")
            
#             return response

        
#         else :
#             msg.append('Incorrect username or password')
#             # raise HTTPException(status_code=400, detail="Incorrect username or password")
#             return templates.TemplateResponse("developer/transaction.html", {"request":request,"msg":msg})
#     except:
#         errors.append('Something wrong')
#         return templates.TemplateResponse("developer/login.html", {"request":request,"msg":msg})


@developer.get('/api-developer-login/')
def login(username1: Optional[str],password1:Optional[str],response:Response):
    username = username1
    password = password1


    user = authenticate_user(username,password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
       
   

    access_token = create_access_token(
                data = {"sub": username,"exp":datetime.utcnow() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)}, 
                expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                                    )

    data = {"sub": username,"exp":datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}
    jwt_token = jwt.encode(data,SECRET_KEY,algorithm=ALGORITHM)
    response.set_cookie(key="access_token", value=f'Bearer {jwt_token}',httponly=True)
    # return response
    
    return {"access_token": jwt_token, "token_type": "bearer"}

# how to get the user through authentication
@developer.get("/current-user/")
async def get_current_user(request:Request):

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
            payload = jwt.decode(param, SECRET_KEY, algorithms=ALGORITHM)
        
            username = payload.get("sub")    
            
            expiration_time = datetime.fromtimestamp(payload.get("exp"))
            # print(expiration_time)
            # print(datetime.utcnow())

            
            if datetime.utcnow() > expiration_time:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired. Please login again.",
                )

            # response_data = {"username": username}
            return username

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Session has expired",
            # headers={"WWW-Authenticate": "Basic"},
        )
 

#======================================Login for Front End or API Login=============================
@developer.get("/developer-login/", response_class=HTMLResponse)
async def api_login(request: Request):
    return templates.TemplateResponse("developer/login.html", {"request":request}) 


@developer.get("/developer-transaction/", response_class=HTMLResponse)
async def developer_login(request: Request, username:str = Depends(get_current_user)):
    return templates.TemplateResponse("developer/transaction.html", {"request":request}) 



@developer.get("/api-developer-employee-credentials")
async def employee_credential_list(username:str = Depends(get_current_user)):
    result = mydb.employee_login.find().sort('fullname', 1)

    employeeData =[{
        "id": str(i['_id']),
        "fullname": i['fullname'],
        "username": i['username'],
        "status": i['status']
    }for i in result]

    return employeeData


@developer.get("/api-developer-admin-credentials")
async def admin_credential_list(username:str = Depends(get_current_user)):
    result = mydb.login.find().sort('fullname', 1)

    employeeData =[{
        "id": str(i['_id']),
        "fullname": i['fullname'],
        "username": i['username'],
        "status": i['status']
    }for i in result]

    return employeeData


@developer.post('/api-insert-login-credential-developer')
async def insert_access_login(item:AccessSetting): # this function is for inserting credential of 
    dataInsert = dict()
    dataInsert = {
        "user_id": item.user_id,
        "username": item.username,
        "accounting_write": item.accounting_write,
        "accounting_read": item.accounting_read,
        "payroll_write": item.payroll_write,
        "payroll_read": item.payroll_read,
        "site_transaction_write": item.site_transaction_write,
        "site_transaction_read": item.site_transaction_read,
        "date_credited": datetime.now(),
        "inventory_write": item.inventory_write,
        "inventory_read": item.inventory_read
 
        }
    mydb.access_setting.insert_one(dataInsert)
