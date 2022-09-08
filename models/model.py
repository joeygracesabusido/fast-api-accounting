from lib2to3.pytree import Base
from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    fullname: str
    username: str
    password: str
    status: str
    created: datetime