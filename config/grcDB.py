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

class GrcEquipment(SQLModel, table=True):
    __tablename__ = 'grc_equipment'
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

class GrcRental(SQLModel, table=True):
    __tablename__ = 'grc_rental'
    id: Optional[int] = Field(default=None, primary_key=True)
    transDate: date
    demr: str = Field(max_length=50)
    equipment_id: str = Field(default=None,index=True)
    timeIn: Optional[datetime] = Field(default=None)
    timeOut: Optional[datetime] = Field(default=None)
    totalHours: condecimal(max_digits=8, decimal_places=2) = Field(default=0)
    rentalRate: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    amount: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    shift: str = Field(default=None)
    driver_operator: str = Field(default=None)
    user: str = Field(default=None)
    date_updated:  Optional[datetime] = Field(default=None)
    date_credited: datetime = Field(default_factory=datetime.utcnow)


    __table_args__ = (Index("idx_grcEquipment_unique", "demr", unique=True),)


class GrcViews():# this is for views function for GRC project

    @staticmethod
    def insertGrcPayrollAdan(transDate,employee_id,first_name,last_name,salaryRate,
                    addOnRate,salaryDetails,regDay,regDayOt,sunday,sundayOT,
                    spl,splOT,lgl2,lgl2OT,nightDiff,adjustment,lgl1,user):
        """This function is for inserting Payroll to  surigaoDB table adan_payroll_grc"""
        insertData = Adan_payroll_grc(transDate=transDate,employee_id=employee_id,first_name=first_name,last_name=last_name,
                                            salaryRate=salaryRate,addOnRate=addOnRate,salaryDetails=salaryDetails,
                                            regDay=regDay,regDayOt=regDayOt,sunday=sunday,sundayOT=sundayOT,spl=spl,
                                            splOT=splOT,lgl2=lgl2,lgl2OT=lgl2OT,nightDiff=nightDiff,adjustment=adjustment,lgl1=lgl1, user=user)


        session = Session(engine)

        session.add(insertData)
        
        session.commit()

        session.close()


    @staticmethod # this is for function get Payroll GRC
    def getPayroll(
        datefrom: Optional[date],
        dateto: Optional[date],
        employeeID: Optional[str] ) : 


        with Session(engine) as session: 
            statement = ''
            
            if employeeID and datefrom == '' and dateto == '':
                statement =  select(Adan_payroll_grc).where(Adan_payroll_grc.employee_id.ilike(f"%{employeeID}%"))

            if datefrom and dateto and employeeID:
                statement =  select(Adan_payroll_grc).where(Adan_payroll_grc.transDate.between(datefrom,dateto),
                                                Adan_payroll_grc.employee_id.ilike(f"%{employeeID}%"))

            if datefrom and dateto and employeeID == '':
                statement =  select(Adan_payroll_grc).where(Adan_payroll_grc.transDate.between(datefrom,dateto)
                                               )

            # elif datefrom =='' and dateto =='' and employeeID =='':
            #     statement = select(Adan_payroll_grc)
            # else:
            #     statement =  select(Adan_payroll_grc).where(Adan_payroll_grc.transDate.between(datefrom,dateto),
            #                                     Adan_payroll_grc.employee_id.ilike(f"%{employeeID}%"))
                        
            results = session.exec(statement) 

            data = results.all()

            
            return data


    @staticmethod
    def insertEquipmentGRC(equipment_id,equipmentDiscription,
                            rentalRate,comments,owners,user):# this function is for inserting Equipment

       
        insertData = GrcEquipment(equipment_id=equipment_id,equipmentDiscription=equipmentDiscription,
                                rentalRate=rentalRate,comments=comments,owners=owners,user=user)


        session = Session(engine)
        
        try:
            session.add(insertData)
            session.commit()
            return {"message": "Data has been saved"}  # Return a success message
        except Exception as e:
            session.rollback()
            error_message = f"Error due to: {str(e)}"
           
            return {"error": error_message}
        finally:
            session.close()

    @staticmethod
    def getEquipment(): # this function is to get all record for equipment in GRC

        with Session(engine) as session:
            statement = select(GrcEquipment)
            results = session.exec(statement) 

            data = results.all()

            
            return data


    @staticmethod
    def insertRentalGRC(transDate,demr,equipment_id,timeIn,timeOut,
                            totalHours,rentalRate,amount,shift,
                                driver_operator,user):# this function is for inserting Equipment

        
        insertData = GrcRental(transDate=transDate,demr=demr,equipment_id=equipment_id,
                                timeIn=timeIn,timeOut=timeOut,totalHours=totalHours,
                                rentalRate=rentalRate,amount=amount,shift=shift,driver_operator=driver_operator,
                                user=user)


        session = Session(engine)
        session.add(insertData)
        session.commit()
        session.close()
      
        # try:
        #     session.add(insertData)
        #     session.commit()
        #     return {"message": "Data has been saved"}  # Return a success message
        # except Exception as e:
        #     session.rollback()
        #     error_message = str(e)  # Use the actual error message from the exception
        #     return {"error": error_message}
        # finally:
        #     session.close()
    @staticmethod
    def getRental( datefrom: Optional[date],
        dateto: Optional[date],
        equipment_id: Optional[str]): # this function is to get all record for rental in GRC

        with Session(engine) as session:
            
            statement = select(GrcRental).where(GrcRental.transDate.between(datefrom,dateto))\
                .filter(GrcRental.equipment_id.like ('%'+ equipment_id +'%')).order_by(GrcRental.id)
            results = session.exec(statement) 

            data = results.all()

            
            return data
    

def create_db_and_tables():
    
    SQLModel.metadata.create_all(engine)

# create_db_and_tables()



