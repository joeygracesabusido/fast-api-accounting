from typing import Optional
from pydantic import condecimal
from sqlmodel import Field, Session, SQLModel, create_engine,select,func,funcfilter,within_group

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


def select_cost(datefrom,dateto,equipment_id):
    """This function is for selecting all data from cost table"""
    with Session(engine) as session:
        statement = select(cost.id,cost.equipment_id,cost.transDate,cost.salaries,cost.fuel,
                        cost.oil_lubes,cost.mechanicalSupplies,cost.repairMaintenance,
                        cost.meals,cost.transpo,cost.tires,cost.amortization,
                        cost.others,cost.totalAmount).where(cost.transDate >= datefrom ,
                         cost.transDate <= dateto ) \
                         .filter(cost.equipment_id.like ('%'+equipment_id +'%')) \
                            .order_by(cost.transDate.asc())
        results = session.exec(statement)

        # func.sum(cost.salaries).label('salaries')
        # .group_by(cost.equipment_id)
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


def select_test():
    """This function is for selecting one data from cost table"""
    with Session(engine) as session:
        # statement = select(func.sum(cost.salaries)).scalar()
        statement = select(cost.equipment_id,func.sum(cost.salaries).label('salaries'),
                    func.sum(cost.fuel).label('fuel'),func.sum(cost.oil_lubes).label('oil_lubes'),
                    func.sum(cost.mechanicalSupplies).label('mechanicalSupplies'),
                    func.sum(cost.repairMaintenance).label('repairMaintenance'),
                    func.sum(cost.meals).label('meals'),func.sum(cost.amortization).label('amortization'),
                    func.sum(cost.tires).label('tires'),func.sum(cost.transpo).label('transpo'),
                    func.sum(cost.others).label('others'),func.sum(cost.totalAmount).label('totalAmount')
                    ).group_by(cost.equipment_id)
        results = session.exec(statement) 


        return results






class cost_entry(SQLModel, table=True): 
    """This is for cost or expenses table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    trans_date: date
    equipment_id: str = Field(index=True)
    clasification: str = Field(default=None)
    cost_amount: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    username: str = Field(default=None)
    update_time: datetime


def selectCostAnalysis2():
    """This is for testing from traditional sql to sqlModel"""

    with Session(engine) as session:
        # statement = select(func.sum(cost.salaries)).scalar()
        statement = select(cost_entry)
                   
        results = session.exec(statement) 

        data = results.all()
        return data

        
      

# create_db_and_tables()