from typing import Optional
from pydantic import condecimal
from sqlmodel import Field, Session, SQLModel, create_engine,select,func,funcfilter,within_group

from datetime import datetime, date
import mysql.connector

import urllib.parse



connection_string = "mysql+pymysql://{user}:{password}@{host}:{port}/{database}".format(
    user="joeysabusido",
    password=urllib.parse.quote("Genesis@11"),
    host="192.46.225.247",
     port=3306,
    database="surigaodb"
)



engine = create_engine(connection_string, echo=True)

class Adan_payroll_grc(SQLModel, table=True):
    __tablename__ = "adan_payroll_grc"  # Specify your desired table name
    id: Optional[int] = Field(default=None, primary_key=True)
    transDate: date
    employee_id: str = Field(index=True)
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    salaryRate: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    addOnRate:  condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    salaryDetails: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    regDay: condecimal(max_digits=5, decimal_places=2) = Field(default=0)
    regDayOt: condecimal(max_digits=5, decimal_places=2) = Field(default=0)
    sunday: condecimal(max_digits=5, decimal_places=2) = Field(default=0)
    sundayOT: condecimal(max_digits=5, decimal_places=2) = Field(default=0)
    spl: condecimal(max_digits=5, decimal_places=2) = Field(default=0)
    splOT: condecimal(max_digits=5, decimal_places=2) = Field(default=0)
    lgl2: condecimal(max_digits=5, decimal_places=2) = Field(default=0)
    lgl2OT: condecimal(max_digits=5, decimal_places=2) = Field(default=0)
    lgl1: condecimal(max_digits=5, decimal_places=2) = Field(default=0)
    nightDiff: condecimal(max_digits=5, decimal_places=2) = Field(default=0)
    adjustment: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    user: str = Field(default=None)
    date_updated:  Optional[datetime] = Field(default=None)
    date_credited: datetime = Field(default_factory=datetime.utcnow)


def create_db_and_tables():
    
    SQLModel.metadata.create_all(engine)

# create_db_and_tables()



