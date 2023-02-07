from typing import Optional
from pydantic import condecimal
from sqlmodel import Field, Session, SQLModel, create_engine,select

from datetime import datetime, date
import mysql.connector

import urllib.parse

# from sqlalchemy.schema import ThreadLocalMetaData as ThreadLocalMetaData



# password = urllib.parse.quote("Genesis@11")


connection_string = "mysql+pymysql://{user}:{password}@{host}:{port}/{database}".format(
    user="joeysabusido",
    password=urllib.parse.quote("Genesis@11"),
    host="192.46.225.247",
     port=3306,
    database="ldglobal"
)



engine = create_engine(connection_string, echo=True)


class cost(SQLModel, table=True): 
    """This is for cost or expenses table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    transDate: date
    equipment_id: str = Field(index=True)
    salaries: condecimal(max_digits=9, decimal_places=3) = Field(default=0)
    fuel: condecimal(max_digits=9, decimal_places=3) = Field(default=0)
    oil_lubes: condecimal(max_digits=9, decimal_places=3) = Field(default=0)
    mechanicalSupplies: condecimal(max_digits=9, decimal_places=3) = Field(default=0)
    repairMaintenance: condecimal(max_digits=9, decimal_places=3) = Field(default=0)
    meals: condecimal(max_digits=9, decimal_places=3) = Field(default=0)
    transpo: condecimal(max_digits=9, decimal_places=3) = Field(default=0)
    tires: condecimal(max_digits=9, decimal_places=3) = Field(default=0)
    amortization: condecimal(max_digits=9, decimal_places=3) = Field(default=0)
    others: condecimal(max_digits=9, decimal_places=3) = Field(default=0)
    totalAmount: condecimal(max_digits=9, decimal_places=3) = Field(default=0)
    user: str
    date_update: datetime = Field(default=None)
    date_created: datetime 

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def insertCost(transDate,equipment_id,salaries,fuel,oil_lubes,
                 mechanicalSupplies, repairMaintenance, meals,transpo,tires, amortization,others, totalAmount,
                 user,date_created):
    """This funtion is for inserting cost or expenses"""
  

    insertData = cost(transDate=transDate, equipment_id=equipment_id,salaries=salaries,
                    fuel=fuel,oil_lubes=oil_lubes, 
                    mechanicalSupplies=mechanicalSupplies,
                    repairMaintenance=repairMaintenance,meals=meals,
                    transpo=transpo,tires=tires,amortization=amortization, 
                    others=others,totalAmount=totalAmount,user=user,date_created=date_created)
    

    session = Session(engine)

    session.add(insertData)
    
    session.commit()

    session.close()


def select_cost(datefrom,dateto):
    """This function is for selecting all data from cost table"""
    with Session(engine) as session:
        statement = select(cost.id,cost.equipment_id,cost.transDate,cost.salaries,cost.fuel,
                        cost.oil_lubes,cost.mechanicalSupplies,cost.repairMaintenance,
                        cost.meals,cost.transpo,cost.tires,cost.amortization,
                        cost.others,cost.totalAmount).where(cost.transDate >= datefrom , cost.transDate <= dateto )
        results = session.exec(statement)
        
        # data = []
        # for x in results:
            
            
        #     data.append(x)
            
        return results

def select_cost_id(id):
    """This function is for selecting one data from cost table"""
    with Session(engine) as session:
        statement = select(cost).where(cost.id == id)
        results = session.exec(statement)

        result = results.one()   
        
        return result

def update_cost(id,transDate,equipment_id,salaries,fuel,oil_lubes,
                 mechanicalSupplies, repairMaintenance, meals,transpo,tires, amortization,others, totalAmount,
                 user,date_update):
    """This function is for updating data from cost table"""
    with Session(engine) as session:
        statement = select(cost).where(cost.id == id)
        results = session.exec(statement)

        result = results.one()

           
        result.transDate = transDate
        result.equipment_id = equipment_id
        result.salaries = salaries
        result.fuel = fuel
        result.oil_lubes = oil_lubes
        result.mechanicalSupplies = mechanicalSupplies
        result.repairMaintenance = repairMaintenance
        result.meals = meals
        result.transpo = transpo
        result.tires = tires
        result.amortization = amortization
        result.others = others
        result.totalAmount = totalAmount
        result.user = user
        result.date_update = date_update

    
        session.add(result)
        session.commit()
        session.refresh(result)


def select_test(equipment_id):
    """This function is for selecting one data from cost table"""
    with Session(engine) as session:
        statement = select(cost).where(cost.equipment_id == equipment_id)
        results = session.exec(statement)
        
         
        
        return results

# create_db_and_tables()