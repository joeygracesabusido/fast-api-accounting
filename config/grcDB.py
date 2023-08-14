from typing import Optional
from pydantic import condecimal
from sqlmodel import Field, Session, SQLModel, create_engine,select,func,funcfilter,within_group

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
            
            if employeeID:
                statement =  select(Adan_payroll_grc).where(Adan_payroll_grc.employee_id.ilike(f"%{employeeID}%"))

            elif datefrom and dateto:
                statement =  select(Adan_payroll_grc).where(Adan_payroll_grc.transDate.between(datefrom,dateto))

            elif datefrom =='' and dateto =='' and employeeID =='':
                statement = select(Adan_payroll_grc)
            else:
                statement =  select(Adan_payroll_grc).where(Adan_payroll_grc.transDate.between(datefrom,dateto),
                                                Adan_payroll_grc.employee_id.ilike(f"%{employeeID}%"))
                        
            results = session.exec(statement) 

            data = results.all()

            
            return data



def create_db_and_tables():
    
    SQLModel.metadata.create_all(engine)

# create_db_and_tables()



