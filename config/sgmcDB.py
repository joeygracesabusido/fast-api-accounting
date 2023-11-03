from typing import Optional
from pydantic import condecimal
from sqlmodel import Field, Session, SQLModel, create_engine,select,func,funcfilter,within_group, Index
from sqlalchemy.exc import SQLAlchemyError

from datetime import datetime, date
import mysql.connector

import urllib.parse

from typing import List



connection_string = "mysql+pymysql://{user}:{password}@{host}:{port}/{database}".format(
    user="joeysabusido",
    password=urllib.parse.quote("Genesis@11"),
    host="192.46.225.247",
     port=3306,
    database="sgmcdb"
)



engine = create_engine(connection_string, echo=True)


class SgmcEquipment(SQLModel, table=True):
    __tablename__ = 'sgmc_equipment'
    id: Optional[int] = Field(default=None, primary_key=True)
    equipment_id: str = Field(default=None)
    equipmentDiscription: str = Field(default=None)
    rentalRate: condecimal(max_digits=8, decimal_places=2) = Field(default=0)
    comments: str = Field(default=None)
    owners: str = Field(default=None)
    user: str = Field(default=None)
    date_updated:  Optional[datetime] = Field(default=None)
    date_credited: datetime = Field(default_factory=datetime.utcnow)


    __table_args__ = (Index("idx_grcEquipment_unique", "equipment_id", unique=True),)


class SgmcRental(SQLModel, table=True):
    __tablename__ = 'sgmc_rental'
    id: Optional[int] = Field(default=None, primary_key=True)
    transDate: date
    eur: str = Field(max_length=50)
    equipment_id: str = Field(default=None,index=True)
    timeIn: condecimal(max_digits=8, decimal_places=2) = Field(default=0)
    timeOut: condecimal(max_digits=8, decimal_places=2) = Field(default=0)
    totalHours: condecimal(max_digits=8, decimal_places=2) = Field(default=0)
    rentalRate: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    amount: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    shift: str = Field(default=None)
    driver_operator: str = Field(default=None)
    user: str = Field(default=None)
    date_updated:  Optional[datetime] = Field(default=None)
    date_credited: datetime = Field(default_factory=datetime.utcnow)


    __table_args__ = (Index("idx_grcEquipment_unique", "eur", unique=True),)

class DieselSgmc(SQLModel, table=True):
    __tablename__ = 'diesel_sgmc'
    id: Optional[int] = Field(default=None, primary_key=True)
    transDate: date
    withdrawal_slip: str = Field(max_length=50)
    equipment_id: str = Field(default=None,index=True)
    literUse: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    price: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    amount: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    user: str = Field(default=None)
    date_updated:  Optional[datetime] = Field(default=None)
    date_credited: datetime = Field(default_factory=datetime.utcnow)

    __table_args__ = (Index("idx_DieselGrc_unique", "withdrawal_slip", unique=True),)




def create_db_and_tables():
    
    SQLModel.metadata.create_all(engine)


class SGMCViews():
    @staticmethod
    def insert_equipment_sgmc(equipment_id,equipmentDiscription,
                            rentalRate,comments,owners,user,date_credited):
         
        insertData = SgmcEquipment(equipment_id=equipment_id,equipmentDiscription=equipmentDiscription,
        rentalRate=rentalRate,comments=comments,owners=owners,user=user,date_credited=date_credited)


        session = Session(engine)
        session.add(insertData)
        session.commit()
        session.close()

    @staticmethod
    def getEquipment(): # this function is to get all record for equipment in GRC

        with Session(engine) as session:
            statement = select(SgmcEquipment)
            results = session.exec(statement) 

            data = results.all()

            
            return data

    @staticmethod
    def insert_rental_sgmc(transDate,demr,equipment_id,timeIn,timeOut,
                            totalHours,rentalRate,amount,shift,
                                driver_operator,user,date_credited):# this function is for inserting Equipment Rental

        
        insertData = SgmcRental(transDate=transDate,demr=demr,equipment_id=equipment_id,
                                timeIn=timeIn,timeOut=timeOut,totalHours=totalHours,
                                rentalRate=rentalRate,amount=amount,shift=shift,driver_operator=driver_operator,
                                user=user,date_credited=date_credited)


        session = Session(engine)
        session.add(insertData)
        session.commit()
        session.close()


# create_db_and_tables()