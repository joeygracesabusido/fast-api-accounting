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

class cost_entry(SQLModel, table=True): 
    """This is for cost or expenses table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    trans_date: date
    equipment_id: str = Field(index=True)
    clasification: str = Field(default=None)
    cost_amount: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    particulars: str = Field(max_length=300,default=None)
    username: str = Field(default=None)
    update_time: datetime


class equipment_details(SQLModel, table=True):
    """This is to create table equipment_details"""
    id: Optional[int] = Field(default=None, primary_key=True)
    equipment_id:  str = Field(index=True)
    purchase_date: date
    description: str = Field(default=None)
    purchase_amount: condecimal(max_digits=18, decimal_places=2) = Field(default=0)
    rental_rate: condecimal(max_digits=18, decimal_places=2) = Field(default=0)
    plate_number: str = Field(default=None)
    status: str = Field(default=None,max_length=250)
    owner: str = Field(default=None,max_length=150)


# ============================================Equipment Rental ===========================================
class equipment_rental(SQLModel, table=True):
    """This is to create table equipment rental"""
    id: Optional[int] = Field(default=None, primary_key=True)
    transaction_id: str = Field(default=None)
    transaction_date: date
    equipment_id:  str = Field(index=True)
    total_rental_hour: condecimal(max_digits=18, decimal_places=2) = Field(default=0)
    rental_rate: condecimal(max_digits=18, decimal_places=2) = Field(default=0)
    rental_amount: condecimal(max_digits=18, decimal_places=2) = Field(default=0)
    username: str = Field(default=None)
    date_update: datetime
    eur_form: str = Field(index=True)
    
class diesel_consumption(SQLModel, table=True):
    """This is to create table diesel_consumption"""
    id: Optional[int] = Field(default=None, primary_key=True)
    transaction_date: date
    equipment_id: str = Field(index=True,default=None,max_length=250)
    withdrawal_slip: str = Field(default=None,max_length=250)
    use_liter: str = Field(default=None,max_length=250)
    price: condecimal(max_digits=18, decimal_places=2) = Field(default=0)
    amount: condecimal(max_digits=18, decimal_places=2) = Field(default=0)
    username: str = Field(default=None,max_length=250)

class hauling_tonnage(SQLModel, table=True):
    """This function is for creating table of Tonnage Rizal"""
    id: Optional[int] = Field(default=None, primary_key=True)
    transDate: date
    equipment_id: str = Field(index=True,default=None,max_length=100)
    tripTicket: str = Field(default=None,max_length=100)
    totalTrip: condecimal(max_digits=18, decimal_places=2) = Field(default=0)
    totalTonnage: condecimal(max_digits=18, decimal_places=2) = Field(default=0)
    rate: condecimal(max_digits=18, decimal_places=2) = Field(default=0)
    amount: condecimal(max_digits=18, decimal_places=2) = Field(default=0)
    driverOperator: str = Field(default=None,max_length=100)
    user: str = Field(default=None,max_length=100)
    date_updated: datetime =  Field(default=None)
    date_credited: datetime



def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# =================================================Cost Frame ================================================
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






#==============================================Cost Entry Test Frame ===============================================


def selectCostAnalysis2():
    """This is for testing from traditional sql to sqlModel"""

    with Session(engine) as session:
        # statement = select(func.sum(cost.salaries)).scalar()
        statement = select(cost_entry)
                   
        results = session.exec(statement) 

        data = results.all()
        return data


#========================================================Equipment Details Frame====================================
def insertEquipment(equipment_id,purchase_date,description,
                        purchase_amount,rental_rate,plate_number,status,owner):
    """This function is for inserting Equipmnet of Rizal """
    insertData = equipment_details(equipment_id=equipment_id,purchase_date=purchase_date,description=description,
                        purchase_amount=purchase_amount,rental_rate=rental_rate,plate_number=plate_number,
                         status=status,owner=owner)
    

    session = Session(engine)

    session.add(insertData)
    
    session.commit()

    session.close()

def getEquipmentRizal():
    """This function is for querying all equipment in Rizal"""
    with Session(engine) as session:
        statement = select(equipment_details).order_by(equipment_details.equipment_id.asc())
                    
        results = session.exec(statement) 

        data = results.all()
        return data


def select_rizalEquipment_id(id):
    """This function is for selecting one data from equipment_details table"""
    with Session(engine) as session:
        statement = select(equipment_details).where(equipment_details.id == id)
        results = session.exec(statement)

        result = results.one()   
        
        return result

def updateRizalequipment(id,equipment_id,purchase_date,description,
                        purchase_amount,rental_rate,plate_number,status,owner):
    """This function is for updating Rizal Equipment"""

    with Session(engine) as session:
        statement = select(equipment_details).where(equipment_details.id == id)
        results = session.exec(statement)

        result = results.one()

           
        result.equipment_id = equipment_id
        result.purchase_date = purchase_date
        result.description = description
        result.purchase_amount = purchase_amount
        result.rental_rate = rental_rate
        result.plate_number = plate_number
        result.status = status
        result.owner = owner
        

    
        session.add(result)
        session.commit()
        session.refresh(result)

#==========================================This is Rental Transaction Frame=========================================    
def insertEquipmentRental(transaction_date,equipment_id,
                        total_rental_hour,rental_rate,rental_amount,username,date_update,eur_form):
    """This function is for inserting Equipmnet of Rizal """
    insertData = equipment_rental(transaction_date=transaction_date,equipment_id=equipment_id,
                            total_rental_hour=total_rental_hour,rental_rate=rental_rate,
                            rental_amount=rental_amount,username=username,date_update=date_update,
                            eur_form=eur_form)
    

    session = Session(engine)

    session.add(insertData)
    
    session.commit()

    session.close()

def getallRental(datefrom,dateto,equipment_id):
    """This function is for queyring all Data fro Rental Transaction Rizal"""
    with Session(engine) as session:
        statement = select(equipment_rental).where(equipment_rental.transaction_date >=datefrom,
        equipment_rental.transaction_date <=dateto,equipment_rental.equipment_id.like ('%'+equipment_id +'%') )
                    
        results = session.exec(statement) 

        data = results.all()
        return data
    
def getallRental_id(id):
    """This function is for queyring all Data fro Rental Transaction Rizal"""
    with Session(engine) as session:
        statement = select(equipment_rental).where(equipment_rental.id == id)
                    
        results = session.exec(statement) 

        data = results.all()
        return data


def updateRentalRizal(id,transaction_date,equipment_id,
                        total_rental_hour,rental_rate,rental_amount,username,date_update,eur_form):
    """This function is for updating Rizal Equipment"""

    with Session(engine) as session:
        statement = select(equipment_rental).where(equipment_rental.id == id)
        results = session.exec(statement)

        result = results.one()

           
        result.transaction_date = transaction_date
        result.equipment_id = equipment_id
        result.total_rental_hour = total_rental_hour
        result.rental_rate = rental_rate
        result.rental_amount = rental_amount
        result.username = username
        result.date_update = date_update
        result.eur_form = eur_form
        

    
        session.add(result)
        session.commit()
        session.refresh(result)
#=============================================Diesel Frame Rizal==================================================
def getAllDiesel_checking(transaction_date,equipment_id,withdrawal_slip):
    """This function is for checking If data are already save"""
    with Session(engine) as session:
        statement = select(diesel_consumption).where(diesel_consumption.transaction_date ==transaction_date,
                                        diesel_consumption.equipment_id.like ('%'+equipment_id +'%'),
                                        diesel_consumption.withdrawal_slip == withdrawal_slip )
                    
        results = session.exec(statement) 

        data = results.all()
        return data


def insertRizalDiesel(transaction_date,equipment_id,withdrawal_slip,
                        use_liter,price,amount,username):
    """This function is for inserting Equipmnet of Rizal """
    insertData = diesel_consumption(transaction_date=transaction_date,
                                        equipment_id=equipment_id,withdrawal_slip=withdrawal_slip,
                                        use_liter=use_liter,price=price,amount=amount,username=username)
    

    session = Session(engine)

    session.add(insertData)
    
    session.commit()

    session.close()

def getallDiesel(datefrom,dateto,equipment_id):
    """This function is for queyring all Data for Diesel Transaction Rizal"""
    with Session(engine) as session:
        statement = select(diesel_consumption).where(diesel_consumption.transaction_date >=datefrom,
        diesel_consumption.transaction_date <=dateto,diesel_consumption.equipment_id.like ('%'+equipment_id +'%') )
                    
        results = session.exec(statement) 

        data = results.all()
        return data
    

def insertTonnageRizal(transDate,equipment_id,tripTicket,
                        totalTrip,totalTonnage,rate,amount,driverOperator,
                        user,date_credited):
    """This function is for Inserting Tonnage Data in Rizal"""
    insertData = hauling_tonnage(transDate=transDate,equipment_id=equipment_id,tripTicket=tripTicket,
                                 totalTrip=totalTrip,totalTonnage=totalTonnage,rate=rate,
                                 amount=amount,driverOperator=driverOperator,user=user,date_credited=date_credited)
    

    session = Session(engine)

    session.add(insertData)
    
    session.commit()

    session.close()

def getallTonnage(datefrom,dateto,equipment_id):
    """This function is for queyring all Data for Diesel Transaction Rizal"""
    with Session(engine) as session:
        statement = select(hauling_tonnage).where(hauling_tonnage.transDate >=datefrom,
        hauling_tonnage.transDate <=dateto,hauling_tonnage.equipment_id.like ('%'+equipment_id +'%') )
                    
        results = session.exec(statement) 

        data = results.all()
        return data


# create_db_and_tables()