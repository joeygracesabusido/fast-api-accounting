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
    project_site: str = Field(default=None,max_length=250)
    remarks: str = Field(default=None,max_length=150)
    owner: str = Field(default=None,max_length=150)


class rentaltransaction(SQLModel, table=True):
    """This is for rental table in TVI"""  
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.d = SQLModel.util._collections.Properties({})

    id: Optional[int] = Field(default=None, primary_key=True)
    transDate: date
    demr: str = Field(default=None)
    equipmentId: str = Field(index=True)
    time_in : datetime = Field(default=None)
    time_out : datetime = Field(default=None)
    totalHours: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    rentalRate: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    totalAmount: condecimal(max_digits=9, decimal_places=2)
    taxRate: condecimal(max_digits=3, decimal_places=2)
    vat_output:  condecimal(max_digits=9, decimal_places=2)
    net_of_vat: condecimal(max_digits=9, decimal_places=2)
    project_site: str = Field(default=None)
    driverOperator: str = Field(default=None)
    user: str = Field(default=None)
    date_updated: datetime = Field(default=None)
    date_credited: datetime

class tvidieseltransaction(SQLModel, table=True):
    """This is for rental table in TVI"""  
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.d = SQLModel.util._collections.Properties({})

    id: Optional[int] = Field(default=None, primary_key=True)
    transDate: date
    equipmentId: str = Field(index=True)
    withdrawalSlip: str = Field(default=None)
    totalliters: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    price: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    totalAmount: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    user: str = Field(default=None)
    date_updated: datetime = Field(default=None)
    date_credited: datetime
    



class tvi_tonnage(SQLModel, table=True):
    """This is for tonnage table in TVI"""
    id: Optional[int] = Field(default=None, primary_key=True)
    transDate: date
    equipmentId: str = Field(index=True)
    tripTicket: str = Field(default=None)
    routes: str = Field(default=None)
    trips: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    volume_tons: condecimal(max_digits=9, decimal_places=2)
    distance: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    hauling_rate: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    project_site: str = Field(default=None)
    driverOperator: str = Field(default=None)
    user: str = Field(default=None)
    date_updated:  Optional[datetime] = Field(default=None)
    date_credited: datetime = Field(default_factory=datetime.utcnow)

class  tviRoutes(SQLModel, table=True):
    """This is for TVI Routes"""
    id: Optional[int] = Field(default=None, primary_key=True)
    routes: str = Field(default=None)
    distance: condecimal(max_digits=3, decimal_places=2) = Field(default=0)

class Adan_payroll_tvi(SQLModel, table=True):
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
    nightDiff: condecimal(max_digits=5, decimal_places=2) = Field(default=0)
    adjustment: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    user: str = Field(default=None)
    date_updated:  Optional[datetime] = Field(default=None)
    date_credited: datetime = Field(default_factory=datetime.utcnow)



def create_db_and_tables2():
    
    SQLModel.metadata.create_all(engine)
    # migrate(engine, SQLModel.metadata)

#============================================This is for Function ======================================
def insertRoutes(routes,distance):
    """This is for inserting Routes in TVI database"""
    insertData = tviRoutes(routes=routes,distance=distance)
    session = Session(engine)

    session.add(insertData)
    
    session.commit()

    session.close()

def getRoutes(routes):
    """This is to query for Routes in TVI """
    with Session(engine) as session:
        statement = select(tviRoutes).filter(tviRoutes.routes.like ('%'+ routes +'%'))
                    
        results = session.exec(statement) 

        data = results.all()
       
        return data

def routesAutocomplete(term):
    """This function is for autocomplete """

    with Session(engine) as session:
        statement = select(tviRoutes).filter(tviRoutes.routes.like ('%'+ term +'%'))
                    
        results = session.exec(statement) 

        data = results.all()
       
        return data
#=======================================this is for Inserting Tonage============================================
def insertTons(transDate,equipmentId,tripTicket,
                 routes,trips,volume_tons,
                  distance, hauling_rate,
                   project_site, driverOperator,user):
    """This function is for Inserting Data into tvi_tonnage Table"""
    insertData = tvi_tonnage(transDate=transDate,equipmentId=equipmentId,tripTicket=tripTicket,
                    routes=routes,trips=trips,volume_tons=volume_tons,distance=distance,
                    hauling_rate=hauling_rate,project_site=project_site,driverOperator=driverOperator,
                    user=user)

    session = Session(engine)

    session.add(insertData)
    
    session.commit()

    session.close()

def getTon(tripTicket):
    """This function is for querying """

    with Session(engine) as session:
        statement = select(tvi_tonnage).filter(tvi_tonnage.tripTicket == tripTicket )
                    
        results = session.exec(statement) 

        data = results.all()
        
        return data

def getTon_id(id):
    """This function is for querying """

    with Session(engine) as session:
        statement = select(tvi_tonnage).filter(tvi_tonnage.id == id)
                    
        results = session.exec(statement) 

        data = results.one()
        
        return data

def updateTons(id,transDate,equipmentId,tripTicket,routes,
                    trips,volume_tons,distance,hauling_rate,project_site,
                    driverOperator,user,date_updated):
    """This function is for updating Rizal Equipment"""

    with Session(engine) as session:
        statement = select(tvi_tonnage).where(tvi_tonnage.id == id)
        results = session.exec(statement)

        result = results.one()

           
        result.transDate = transDate
        result.equipmentId = equipmentId
        result.tripTicket = tripTicket
        result.routes = routes
        result.trips = trips
        result.volume_tons = volume_tons
        result.distance = distance
        result.hauling_rate = hauling_rate
        result.project_site = project_site
        result.driverOperator = driverOperator
        result.user = user
        result.date_updated = date_updated

        

    
        session.add(result)
        session.commit()
        session.refresh(result)

def getIncentives(datefrom,dateto,equipmentId):
    """This function is for querying Incentive """
    with Session(engine) as session:
        statement = select(tvi_tonnage.equipmentId,
                func.sum(tvi_tonnage.trips).label('trips'),
                tvi_tonnage.routes,tvi_tonnage.distance,tvi_tonnage.driverOperator
                ).where(tvi_tonnage.transDate.between(datefrom,dateto)
                ).filter(tvi_tonnage.equipmentId.like ('%'+ equipmentId +'%')) \
                .group_by(tvi_tonnage.equipmentId,tvi_tonnage.routes,tvi_tonnage.distance,tvi_tonnage.driverOperator)

        results = session.exec(statement) 

        data = results.all()

        
        return data
    

def getTons(datefrom,dateto,equipmentId,project_site):
    """This function is for querying all Rental Equipment in TVI"""
    with Session(engine) as session:
        statement = select(tvi_tonnage).where(tvi_tonnage.transDate.between(datefrom,dateto)) \
                        .filter(tvi_tonnage.equipmentId.like ('%'+ equipmentId +'%'),tvi_tonnage.project_site.like ('%'+ project_site +'%')) \
                         .order_by(tvi_tonnage.transDate.asc())
                    
        results = session.exec(statement) 

        data = results.all()

        
        return data


#=====================================This is for Equipment Model=============================================

def insertEquipment_tvi(equipmentID,purchase_date,equipmentDesc,
                        purchase_amount,rentalRate,plate_number,status, project_site ,remarks,owner):
    """This function is for inserting Equipmnet of Rizal """
    insertData = equipment_details_tvi(equipmentID=equipmentID,purchase_date=purchase_date,
                    equipmentDesc=equipmentDesc,purchase_amount=purchase_amount,
                    rentalRate=rentalRate,plate_number=plate_number,status=status,project_site=project_site,
                     remarks=remarks,owner=owner)
    

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
            " project_site ": x. project_site,
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
                        purchase_amount,rentalRate,plate_number,status,remarks,owner,project_site):
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
        result.project_site = project_site
        result.status = status
        result.remarks = remarks
        result.owner = owner
        

    
        session.add(result)
        session.commit()
        session.refresh(result)


#=====================================================TVI Rental Frame =======================================
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
    """This function is for querying all equipment in TVI"""
    with Session(engine) as session:
        statement = select(rentaltransaction).order_by(rentaltransaction.id.asc())
                    
        results = session.exec(statement) 

        data = results.all()

        
        return data

def getRentalTVI_id_update(id):
    """This function is for querying all equipment in TVI"""
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

def getRentalTVI_all_employeeLogin(datefrom,dateto,equipmentId,project_site):
    """This function is for querying all Rental Equipment in TVI"""
    with Session(engine) as session:
        statement = select(rentaltransaction).where(rentaltransaction.transDate >= datefrom ,
                         rentaltransaction.transDate <= dateto ) \
                        .filter(rentaltransaction.equipmentId.like ('%'+ equipmentId +'%'),rentaltransaction.project_site.like ('%'+ project_site +'%')) \
                         .order_by(rentaltransaction.id.asc())
                    
        results = session.exec(statement) 

        data = results.all()

        
        return data

def deleteRental(id):
    """This function is to delete record for Rental Transaction"""
    with Session(engine) as session:
        statement = select(rentaltransaction).where(rentaltransaction.id == id)
        results = session.exec(statement)
        result = results.one()
       

        session.delete(result)
        session.commit()


def rentalSumTVI(datefrom,dateto,equipmentId):
    """This function is for selecting SUM for Rental Record"""
    with Session(engine) as session:
        # statement = select(func.sum(cost.salaries)).scalar()
        statement = select(rentaltransaction.equipmentId,
                    func.sum(rentaltransaction.totalHours).label('totalHours'),
                    rentaltransaction.rentalRate).where(rentaltransaction.transDate >= datefrom ,
                         rentaltransaction.transDate <= dateto
                    ).filter(rentaltransaction.equipmentId.like ('%'+ equipmentId +'%')) \
                    .group_by(rentaltransaction.equipmentId,rentaltransaction.rentalRate)
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

def insertRental_tvi_employeeLogin(transDate, demr,equipmentId, time_in,time_out,totalHours,
                       rentalRate,totalAmount,taxRate,vat_output,net_of_vat,project_site,
                       driverOperator,user,date_credited):
    """This function is for inserting Rental Transaction in TVI """
    
    insertData = rentaltransaction(transDate=transDate,demr=demr, equipmentId=equipmentId,
                    time_in=time_in,time_out=time_out,totalHours=totalHours,rentalRate=rentalRate,
                    totalAmount=totalAmount,taxRate=taxRate,
                    vat_output=vat_output,net_of_vat=net_of_vat,
                    project_site=project_site, driverOperator=driverOperator,
                    user=user,date_credited=date_credited)
    

    session = Session(engine)

    session.add(insertData)
    
    session.commit()

    session.close()

def updateTVIrental(id,transDate,demr,equipmentId,totalHours,
                       rentalRate,totalAmount,taxRate,vat_output,net_of_vat,project_site,
                       driverOperator,user,date_updated):
    """This function is for updating Rizal Equipment"""

    with Session(engine) as session:
        statement = select(rentaltransaction).where(rentaltransaction.id == id)
        results = session.exec(statement)

        result = results.one()

           
        result.transDate = transDate
        result.demr = demr
        result.equipmentId = equipmentId
        result.totalHours = totalHours
        result.rentalRate = rentalRate
        result.totalAmount = totalAmount
        result.taxRate = taxRate
        result.vat_output = vat_output
        result.net_of_vat = net_of_vat
        result.project_site = project_site
        result.driverOperator = driverOperator
        result.user = user
        result.date_updated = date_updated
        

    
        session.add(result)
        session.commit()
        session.refresh(result) 


#===================================================TVI Diesel Transaction ====================================
def insertDiesel_tvi(transDate,equipmentId,withdrawalSlip,
                        totalliters,price,totalAmount,user,date_credited):
    """This function is for inserting Rental Transaction in TVI """
    
    insertData = tvidieseltransaction(transDate=transDate,equipmentId=equipmentId,withdrawalSlip=withdrawalSlip,
                                        totalliters=totalliters,price=price,
                                        totalAmount=totalAmount,user=user,date_credited=date_credited)
    

    session = Session(engine)

    session.add(insertData)
    
    session.commit()

    session.close()

def getDieselTVI_all(datefrom,dateto,equipmentId):
    """This function is for querying all equipment in Rizal"""
    with Session(engine) as session:
        statement = select(tvidieseltransaction).where(tvidieseltransaction.transDate >= datefrom ,
                         tvidieseltransaction.transDate <= dateto ) \
                         .filter(tvidieseltransaction.equipmentId.like ('%'+ equipmentId +'%')) \
                         .order_by(tvidieseltransaction.id.asc())
                    
        results = session.exec(statement) 

        data = results.all()

        
        return data


def getDieselTVI_id(id):
    """This function is for querying all equipment in Rizal"""
    with Session(engine) as session:
        

        statement = select(tvidieseltransaction).where(tvidieseltransaction.id == id)
                    
        results = session.exec(statement) 

        data = results.all()
       
        return data

def getDieselTVI_withSlip(withdrawalSlip):
    """This function is for querying all equipment in Rizal"""
    with Session(engine) as session:
        

        statement = select(tvidieseltransaction).where(tvidieseltransaction.withdrawalSlip == withdrawalSlip)
                    
        results = session.exec(statement) 

        data = results.all()
       
        return data

def DiesellSumTVI(datefrom,dateto):
    """This function is for selecting SUM for Diesel Record"""
    with Session(engine) as session:
        # statement = select(func.sum(cost.salaries)).scalar()
        statement = select(tvidieseltransaction.equipmentId,
                    func.sum(tvidieseltransaction.totalliters).label('totalliters'),
                    func.sum(tvidieseltransaction.totalAmount).label('totalAmount')) \
                    .where(tvidieseltransaction.transDate >= datefrom ,
                         tvidieseltransaction.transDate <= dateto
                    ) \
                    .group_by(tvidieseltransaction.equipmentId)
        results = session.exec(statement) 

        data = results.all()
        return data


def updateTVIDiesel(id,transDate,equipmentId,withdrawalSlip,
                        totalliters,price,totalAmount,user,date_updated):
    """This function is for updating Rizal Equipment"""

    with Session(engine) as session:
        statement = select(tvidieseltransaction).where(tvidieseltransaction.id == id)
        results = session.exec(statement)

        result = results.one()

           
        result.transDate = transDate
        result.equipmentId = equipmentId
        result.withdrawalSlip = withdrawalSlip
        result.totalliters = totalliters
        result.price = price
        result.totalAmount = totalAmount
        result.user = user
        result.date_updated = date_updated
        

    
        session.add(result)
        session.commit()
        session.refresh(result) 

#===========================================This is for TVI Payroll =============================================
def insertPayroll(transDate,employee_id,first_name,last_name,salaryRate,
                    addOnRate,salaryDetails,regDay,regDayOt,sunday,sundayOT,
                    spl,splOT,lgl2,lgl2OT,nightDiff,adjustment,user):
    """This is for inserting Payroll Transaction"""
    insertData = Adan_payroll_tvi(transDate=transDate,employee_id=employee_id,first_name=first_name,last_name=last_name,
                                        salaryRate=salaryRate,addOnRate=addOnRate,salaryDetails=salaryDetails,
                                        regDay=regDay,regDayOt=regDayOt,sunday=sunday,sundayOT=sundayOT,spl=spl,
                                        splOT=splOT,lgl2=lgl2,lgl2OT=lgl2OT,nightDiff=nightDiff,adjustment=adjustment,user=user)


    session = Session(engine)

    session.add(insertData)
    
    session.commit()

    session.close()

def getPayrollTvi(datefrom,dateto):
    """This function is for querying Payroll in TVI adan"""
    with Session(engine) as session:
        statement = select(Adan_payroll_tvi).where(Adan_payroll_tvi.transDate.between(datefrom,dateto)) \
                         .order_by(Adan_payroll_tvi.id.asc())
                    
        results = session.exec(statement) 

        data = results.all()

        
        return data
def getPayrollTvi_id(id):
    """This function is for querying all TVI payroll"""
    with Session(engine) as session:
        

        statement = select(Adan_payroll_tvi).where(Adan_payroll_tvi.id == id)
                    
        results = session.exec(statement) 

        data = results.one()
       
        return data

# getRentalTVI_id('181')
# select_tivEquipment_with_id(1)
# getEquipmentTVI2()
# getRentalTVI()


# create_db_and_tables2()

