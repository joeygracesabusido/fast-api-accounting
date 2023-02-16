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


class rentaltransaction(SQLModel, table=True):
    """This is for rental table in TVI"""  
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.d = SQLModel.util._collections.Properties({})

    id: Optional[int] = Field(default=None, primary_key=True)
    transDate: date
    equipmentId: str = Field(index=True,unique=True)
    totalHours: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    rentalRate: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    totalAmount: condecimal(max_digits=9, decimal_places=2)
    taxRate: condecimal(max_digits=3, decimal_places=2)
    vat_output:  condecimal(max_digits=9, decimal_places=2)
    net_of_vat: condecimal(max_digits=9, decimal_places=2)
    driverOperator: str = Field(default=None)
    user: str = Field(default=None)
    date_updated: datetime = Field(default=None)
    date_credited: datetime

    

    


def create_db_and_tables2():
    
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

        print(data)
        return data


def getEquipmentTVI2():
    """This function is for querying all equipment in Rizal"""
    with Session(engine) as session:
        statement = select(equipment_details_tvi)
                    
        results = session.exec(statement) 

        
        equipmentData = [
        {
            "id": x.id,
            "equipmentID": x.equipmentID,
            "purchase_date": x.purchase_date,
            "equipmentDesc": x.equipmentDesc,
            "purchase_amount": x.purchase_amount,
            "rentalRate": x.rentalRate,
            "plate_number": x.plate_number,
            "status": x.status,
            "remarks": x.remarks,
            "owner": x.owner,
        }
        for x in results
            
        ]

      
                
        return equipmentData  



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
        for i in result:
            print(i)
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


#=============================================TVI Frame=======================================
def getRentalTVI_id(term):
    """This function is for querying all equipment in Rizal"""
    with Session(engine) as session:
        # statement = select(equipment_details_tvi).filter(equipment_details_tvi.equipmentID.like ('%'+ term +'%')) \
        #                     .order_by(equipment_details_tvi.equipmentID.asc())

        statement = select(equipment_details_tvi).filter(equipment_details_tvi.equipmentID.like ('%'+ term +'%'))
                    
        results = session.exec(statement) 

        data = results.all()
       
        return data

def getRentalTVI():
    """This function is for querying all equipment in Rizal"""
    with Session(engine) as session:
        statement = select(rentaltransaction).order_by(rentaltransaction.id.asc())
                    
        results = session.exec(statement) 

        data = results.all()

        
        return data

def getRentalTVI_id_update(id):
    """This function is for querying all equipment in Rizal"""
    with Session(engine) as session:
        statement = select(rentaltransaction).where(rentaltransaction.id == id)
                    
        results = session.exec(statement) 

        data = results.all()

        
        return data


def getRentalTVI_all(datefrom,dateto,equipmentId):
    """This function is for querying all equipment in Rizal"""
    with Session(engine) as session:
        statement = select(rentaltransaction).where(rentaltransaction.transDate >= datefrom ,
                         rentaltransaction.transDate <= dateto ) \
                         .filter(rentaltransaction.equipmentId.like ('%'+ equipmentId +'%')) \
                         .order_by(rentaltransaction.id.asc())
                    
        results = session.exec(statement) 

        data = results.all()

        
        return data


def insertRental_tvi(transDate,equipmentId,totalHours,
                       rentalRate,totalAmount,taxRate,vat_output,net_of_vat,
                       driverOperator,user,date_credited):
    """This function is for inserting Rental Transaction in TVI """
    
    insertData = rentaltransaction(transDate=transDate,equipmentId=equipmentId,
                    totalHours=totalHours,rentalRate=rentalRate,
                    totalAmount=totalAmount,taxRate=taxRate,
                    vat_output=vat_output,net_of_vat=net_of_vat,driverOperator=driverOperator,
                    user=user,date_credited=date_credited)
    

    session = Session(engine)

    session.add(insertData)
    
    session.commit()

    session.close()

def updateTVIrental(id,transDate,equipmentId,totalHours,
                       rentalRate,totalAmount,taxRate,vat_output,net_of_vat,
                       driverOperator,user,date_updated):
    """This function is for updating Rizal Equipment"""

    with Session(engine) as session:
        statement = select(rentaltransaction).where(rentaltransaction.id == id)
        results = session.exec(statement)

        result = results.one()

           
        result.transDate = transDate
        result.equipmentId = equipmentId
        result.totalHours = totalHours
        result.rentalRate = rentalRate
        result.totalAmount = totalAmount
        result.taxRate = taxRate
        result.vat_output = vat_output
        result.net_of_vat = net_of_vat
        result.driverOperator = driverOperator
        result.user = user
        result.date_updated = date_updated
        

    
        session.add(result)
        session.commit()
        session.refresh(result) 


# getRentalTVI_id('181')
# select_tivEquipment_with_id(1)
# getEquipmentTVI2()
# getRentalTVI()



# create_db_and_tables2()

