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
    database="ldTviDB"
)

engine = create_engine(connection_string, echo=True)


class equipment_details_tvi(SQLModel, table=True):
    """This is to create table equipment_details"""
    id: Optional[int] = Field(default=None, primary_key=True)
    equipmentID:  str = Field(index=True,unique=True)
    purchase_date: date
    equipmentDesc: str = Field(default=None)
    purchase_amount: condecimal(max_digits=18, decimal_places=2) = Field(default=0)
    rentalRate: condecimal(max_digits=18, decimal_places=2) = Field(default=0)
    plate_number: str = Field(default=None)
    status: str = Field(default=None,max_length=250)
    remarks: str = Field(default=None,max_length=150)
    owner: str = Field(default=None,max_length=150)
    

def create_db_and_tables():
    
    SQLModel.metadata.create_all(engine)


def insertEquipment_tvi(equipmentID,purchase_date,equipmentDesc,
                        purchase_amount,rentalRate,plate_number,status,remarks,owner):
    """This function is for inserting Equipmnet of Rizal """
    insertData = equipment_details_tvi(equipmentID=equipmentID,purchase_date=purchase_date,
                    equipmentDesc=equipmentDesc,purchase_amount=purchase_amount,
                    rentalRate=rentalRate,plate_number=plate_number,status=status,remarks=remarks,
                    owner=owner)
    

    session = Session(engine)

    session.add(insertData)
    
    session.commit()

    session.close()


def getEquipmentTVI():
    """This function is for querying all equipment in Rizal"""
    with Session(engine) as session:
        statement = select(equipment_details_tvi).order_by(equipment_details_tvi.equipmentID.asc())
                    
        results = session.exec(statement) 

        data = results.all()
        return data

def select_tivEquipment_id(equipmentID):
    """This function is for selecting one data from equipment_details table"""
    with Session(engine) as session:
        statement = select(equipment_details_tvi).where(equipment_details_tvi.equipmentID == equipmentID)
        results = session.exec(statement)

        result = results.one()   
        
        return result


def select_tivEquipment_with_id(id):
    """This function is for selecting one data from equipment_details table"""
    with Session(engine) as session:
        statement = select(equipment_details_tvi).where(equipment_details_tvi.id == id)
        
        results = session.exec(statement)

        result = results.one()   
        
        return result


def updateTVIequipment(id,equipmentID,purchase_date,equipmentDesc,
                        purchase_amount,rentalRate,plate_number,status,remarks,owner):
    """This function is for updating Rizal Equipment"""

    with Session(engine) as session:
        statement = select(equipment_details_tvi).where(equipment_details_tvi.id == id)
        results = session.exec(statement)

        result = results.one()

           
        result.equipmentID = equipmentID
        result.purchase_date = purchase_date
        result.equipmentDesc = equipmentDesc
        result.purchase_amount = purchase_amount
        result.rentalRate = rentalRate
        result.plate_number = plate_number
        result.status = status
        result.remarks = remarks
        result.owner = owner
        

    
        session.add(result)
        session.commit()
        session.refresh(result)


# create_db_and_tables()