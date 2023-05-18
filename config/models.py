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

class employee_details(SQLModel, table=True):
    """This is for employe Table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: str = Field(index=True)
    lastName: str = Field(default=None)
    firstName: str = Field(default=None)
    middleName: str = Field(default=None)
    address_employee: str = Field(default=None)
    contactNumber: str = Field(default=None)
    contact_person: str = Field(default=None)
    emer_cont_person: str = Field(default=None)
    position: str = Field(default=None)
    date_hired: date
    department: str = Field(default=None)
    end_contract: date
    tin: str = Field(default=None)
    sssNumber: str = Field(default=None)
    phicNumber: str = Field(default=None)
    hdmfNumber: str = Field(default=None)
    employment_status: str = Field(default=None)
    update_contract: str = Field(default=None)
    salary_rate: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    taxCode: str = Field(default=None)
    Salary_Detail: str = Field(default=None)
    off_on_details: str = Field(default=None)
    user: str = Field(default=None)
    update_date: datetime


class sss_table(SQLModel, table=True):
    """SSS Table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    amountFrom: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    amountTo: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    empShare : condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    mandtoryProvi: condecimal(max_digits=9, decimal_places=2) = Field(default=0)


class payroll_computation(SQLModel, table=True):
    """Payroll Computation"""
    id: Optional[int] = Field(default=None, primary_key=True)
    department: str = Field(default=None,max_length=250)
    cut_off_date: date
    employee_id: str = Field(default=None,max_length=80)
    last_name: str = Field(default=None,max_length=80)
    first_name: str = Field(default=None,max_length=80)
    position_name: str = Field(default=None,max_length=100)
    salary_rate: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    provicaial_rate: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    regular_day: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    regularday_cal: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    regularday_ot: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    regularday_ot_cal: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    regularsunday: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    regularsunday_cal: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    regularsunday_ot: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    regularsunday_ot_cal: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    spl: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    spl_cal: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    spl_ot: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    spl_ot_cal: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    legal_day: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    legal_day_cal: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    legal_day_ot: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    legal_day_ot_cal: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    shoprate_day: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    shoprate_day_cal:condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    proviRate_day: condecimal(max_digits=9, decimal_places=2) = Field(default=0) 
    proviRate_day_cal: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    proviRate_day_ot: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    proviRate_day_ot_cal: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    provisun_day: condecimal(max_digits=9, decimal_places=2) = Field(default=0) 
    provisun_day_cal: condecimal(max_digits=9, decimal_places=2) = Field(default=0) 
    provisun_day_ot: condecimal(max_digits=9, decimal_places=2) = Field(default=0) 
    provisun_day_ot_cal: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    nightdiff_day: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    nightdiff_day_cal: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    adjustment: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    adjustment_cal: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    grosspay_save: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    salaryDetails_save: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    sss_save: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    phic_save: condecimal(max_digits=9, decimal_places=2) = Field(default=0) 
    hmdf_save: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    sss_provi_save: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    total_mandatory: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    uniform_save: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    rice_save: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    laundry_save: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    medical1_save: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    medical2_save: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    totalDem_save: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    otherforms_save: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    taxable_amount: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    taxwitheld_save: condecimal(max_digits=9, decimal_places=2) = Field(default=0)  
    cashadvance_save: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    sssloan_save: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    hdmfloan_save: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    netpay_save: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    taxable_mwe_detail: condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    on_off_details: condecimal(max_digits=9, decimal_places=2) = Field(default=0)     
    userlog: str = Field(default=None,max_length=50)
    time_update: datetime

class tax_table(SQLModel, table=True):
    """This is for Taxable"""
    id: Optional[int] = Field(default=None, primary_key=True)
    amountFrom : condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    amountTo : condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    amountbase : condecimal(max_digits=9, decimal_places=2) = Field(default=0)
    percentageAmount : condecimal(max_digits=9, decimal_places=2) = Field(default=0)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

#================================================Employee Details=================================
def getAllEmployee_TVI():
    """This function is for querying all equipment in Rizal"""
    with Session(engine) as session: 
        project1 = 'Bayug'
        project2 = 'Zamboanga'
        filter_condition = ((employee_details.department.like ('%'+project1 +'%')) |
                             (employee_details.department.like ('%'+project2 +'%')))
        statement = select(employee_details).where(filter_condition) \
        .order_by(employee_details.lastName.asc())
                    
        results = session.exec(statement) 

        data = results.all()

        
        return data





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
    """This function is for selecting one data from equipment_details table """
    with Session(engine) as session:
        statement = select(equipment_details).where(equipment_details.id == id)
        results = session.exec(statement)

        result = results.one()   
        
        return result

def select_rizalEquipment(equipment_id):
    """This function is for selecting one data from equipment_details table using equipment ID"""
    with Session(engine) as session:
        statement = select(equipment_details).where(equipment_details.equipment_id == equipment_id)
        results = session.exec(statement)

        result = results.all()   
        
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

def getallRentalCheck(dateSearch,equipment_id,eur_form,total_rental_hour):
    """This function is for checking if data has already been save in Rental Transaction Rizal"""
    with Session(engine) as session:
        statement = select(equipment_rental).where(equipment_rental.transaction_date == dateSearch,
        equipment_rental.equipment_id == equipment_id,equipment_rental.eur_form == eur_form,
        equipment_rental.total_rental_hour == total_rental_hour)
                    
        results = session.exec(statement) 

        data = results.all()
        return data

def getallRental(datefrom,dateto,equipment_id):
    """This function is for queyring all Data fro Rental Transaction Rizal"""
    with Session(engine) as session:
        statement = select(equipment_rental).where(equipment_rental.transaction_date >=datefrom,
        equipment_rental.transaction_date <=dateto,equipment_rental.equipment_id.like ('%'+equipment_id +'%') )
                    
        results = session.exec(statement) 

        data = results.all()
        return data



def getChartRental(datefrom, dateto):
    """This function is querying for Line chart for Rental Transactions"""
    with Session(engine) as session:
        statement = select(equipment_rental.transaction_date,
                            func.sum(equipment_rental.total_rental_hour).label('totalHours'),
                        ).where(equipment_rental.transaction_date.between(datefrom, dateto)).\
                        group_by(equipment_rental.transaction_date).\
                        order_by(equipment_rental.transaction_date)
        results = session.execute(statement)
        data = results.all()
        return data
    

def getMonthlyRental():
    with Session(engine) as session:
        statement = select(func.DATE_FORMAT(equipment_rental.transaction_date, '%Y-%m').label('month_year'),
                            func.sum(equipment_rental.total_rental_hour).label('total_hours'),
                        ).group_by('month_year').order_by('month_year')
        results = session.execute(statement)
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

def rentalSumRizal(datefrom,dateto,equipment_id):
    """This function is for selecting SUM for Rental Record"""
    with Session(engine) as session:
        # statement = select(func.sum(cost.salaries)).scalar()
        statement = select(equipment_rental.equipment_id,
                    func.sum(equipment_rental.total_rental_hour).label('totalHours'),
                    equipment_rental.rental_rate).where(equipment_rental.transaction_date >= datefrom ,
                         equipment_rental.transaction_date <= dateto
                    ).filter(equipment_rental.equipment_id.like ('%'+ equipment_id +'%')) \
                    .group_by(equipment_rental.equipment_id,equipment_rental.rental_rate) \
                        .order_by(equipment_rental.equipment_id)
        results = session.exec(statement) 

        data = results.all()
        return data

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

def dieselSumRizal(datefrom,dateto,equipment_id):
    """This function is for selecting SUM for Diesel Record"""
    with Session(engine) as session:
        # statement = select(func.sum(cost.salaries)).scalar()
        statement = select(diesel_consumption.equipment_id,
                    func.sum(diesel_consumption.use_liter).label('use_liter'),
                    func.sum(diesel_consumption.amount).label('amount')) \
                    .where(diesel_consumption.transaction_date >= datefrom ,
                         diesel_consumption.transaction_date <= dateto
                    ).filter(diesel_consumption.equipment_id.like ('%'+ equipment_id +'%')) \
                    .group_by(diesel_consumption.equipment_id) \
                        .order_by(diesel_consumption.equipment_id)
        results = session.exec(statement) 

        data = results.all()
        return data
    
#=================================================Tonnage Frame================================================
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
        hauling_tonnage.transDate <=dateto,hauling_tonnage.equipment_id.like ('%'+equipment_id +'%')).order_by(hauling_tonnage.transDate.asc())
                    
        results = session.exec(statement) 

        data = results.all()
        return data
def getAllTonnage_checking(tripTicket):
    """This function is for checking If data are already save"""
    with Session(engine) as session:
        statement = select(hauling_tonnage).where(hauling_tonnage.tripTicket.like ('%'+tripTicket +'%'))
                    
        results = session.exec(statement) 

        data = results.all()
        return data

def tonnageSumRizal(datefrom,dateto,equipment_id):
    """This function is for selecting SUM for Tonnage Record"""
    with Session(engine) as session:
        # statement = select(func.sum(cost.salaries)).scalar()
        statement = select(hauling_tonnage.equipment_id,
                    func.sum(hauling_tonnage.totalTonnage).label('totalTons'),
                    hauling_tonnage.rate).where(hauling_tonnage.transDate >= datefrom ,
                         hauling_tonnage.transDate <= dateto
                    ).filter(hauling_tonnage.equipment_id.like ('%'+ equipment_id +'%')) \
                    .group_by(hauling_tonnage.equipment_id,hauling_tonnage.rate) \
                        .order_by(hauling_tonnage.equipment_id)
        results = session.exec(statement) 

        data = results.all()
        return data


#=========================================This is for SSS Table ======================================
def getSSSTable():
    """This is for querying SSS Table"""
    with Session(engine) as session:
        statement = select(sss_table) \
                        .order_by(sss_table.id)
        results = session.exec(statement) 

        data = results.all()
        return data

#============================================This is for Payroll Transaction============================
def getPayrollTransactions(datefrom,dateto,department,on_off_details):
    """This function is for querying for payroll Computation Transaction"""
    with Session(engine) as session:
        statement = select(payroll_computation.id,payroll_computation.employee_id,
                        payroll_computation.first_name,payroll_computation.last_name, payroll_computation.position_name,
                        payroll_computation.salary_rate,payroll_computation.grosspay_save,
                        payroll_computation.department,payroll_computation.totalDem_save,
                        payroll_computation.otherforms_save,payroll_computation.taxable_amount,
                        payroll_computation.total_mandatory,payroll_computation.taxable_mwe_detail,
                        payroll_computation.sss_save,payroll_computation.phic_save,
                        payroll_computation.hmdf_save,payroll_computation.cut_off_date,
                        ) \
                        .where(payroll_computation.cut_off_date.between(datefrom,dateto)
                        ,payroll_computation.department.like ('%'+ department +'%'),
                        payroll_computation.on_off_details.like ('%'+ on_off_details +'%') )

        results = session.exec(statement) 

        data = results.all()
        return data
#==========================================This is for Payroll===============================================
def taxAmount():
    """This is for Quarying for Tax table"""
    with Session(engine) as session:
        statement = select(tax_table.id,tax_table.amountFrom,
                        tax_table.amountTo,tax_table.amountbase, tax_table.percentageAmount,
                        ).order_by(tax_table.id)

        results = session.exec(statement) 

        data = results.all()
        return data


def testJoinTable(datefrom,dateto):
    """This function is for Testing Joining Table using sqlmodel"""
    with Session(engine) as session:
        subquery_tc = (
            select(
                cost.equipment_id,
                func.sum(cost.totalAmount).label("totalCost")
            )
            .where((cost.transDate >= datefrom) & (cost.transDate <= dateto))
            .group_by(cost.equipment_id)
            .subquery()
        )

        subquery_ht = (
            select(
                hauling_tonnage.equipment_id,
                func.sum(hauling_tonnage.amount).label("totalTonAmount")
            )
            .where((hauling_tonnage.transDate >= datefrom) & (hauling_tonnage.transDate <= dateto))
            .group_by(hauling_tonnage.equipment_id)
            .subquery()
        )

        subquery_er = (
            select(
                equipment_rental.equipment_id,
                func.sum(equipment_rental.rental_amount).label("totalRentalAmount")
            )
            .where((equipment_rental.transaction_date >= datefrom) & (equipment_rental.transaction_date <= dateto))
            .group_by(equipment_rental.equipment_id)
            .subquery()
        )

        subquery_dc = (
            select(
                diesel_consumption.equipment_id,
                func.sum(diesel_consumption.amount).label("totalDCamount")
            )
            .where((diesel_consumption.transaction_date >= datefrom) & (diesel_consumption.transaction_date <= dateto))
            .group_by(diesel_consumption.equipment_id)
            .subquery()
        )

        statement = (
            select(
                equipment_details.equipment_id,
                func.coalesce(subquery_ht.c.totalTonAmount, 0).label("TonAmount"),
                func.coalesce(subquery_er.c.totalRentalAmount, 0).label("RentalAmount"),
                func.coalesce(subquery_dc.c.totalDCamount, 0).label("DieselAmount"),
                func.coalesce(subquery_tc.c.totalCost, 0).label("Expenses")
            )
            .select_from(equipment_details)
            .outerjoin(subquery_tc, equipment_details.equipment_id == subquery_tc.c.equipment_id)
            .outerjoin(subquery_ht, equipment_details.equipment_id == subquery_ht.c.equipment_id)
            .outerjoin(subquery_er, equipment_details.equipment_id == subquery_er.c.equipment_id)
            .outerjoin(subquery_dc, equipment_details.equipment_id == subquery_dc.c.equipment_id)
            .order_by(equipment_details.equipment_id)
        )

        results = session.exec(statement)
        data = results.all()
        return data





# create_db_and_tables()