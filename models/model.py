from lib2to3.pytree import Base
from pydantic import BaseModel
from datetime import datetime, date

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from typing import Optional, List

# from config.database import Base

class User(BaseModel):
    fullname: str
    username: str
    password: str
    status: str
    created: datetime

class EmployeeUser(BaseModel):
    fullname: str
    username: str
    password: str
    status: str
    created: datetime

class balansheetType(BaseModel):
    bstype: str

class ChartofAccount(BaseModel):
    accountNum: str
    accountTitle: str
    bsClass: str
    user: str
    created: datetime

class JournalEntry(BaseModel):
    date_entry: date
    journal: str
    ref: str
    descriptions: str
    acoount_number: str
    account_disc: str
    bsClass: str
    debit_amount: float
    credit_amount: float
    due_date_apv: date
    terms_days: int
    supplier_Client: str
    user: str
    created:datetime

class UpdateJVEntry_surigao(BaseModel):
    date_entry: datetime
    journal: str
    ref: str
    descriptions: str
    acoount_number: str
    account_disc: str
    bsClass: str
    debit_amount: float
    credit_amount: float
    user: str
    created: datetime

# ================================================Zamboanga Accouting Transaction=======================
class UpdateJVEntry_zamboanga(BaseModel):
    date_entry: datetime
    journal: str
    ref: str
    descriptions: str
    acoount_number: str
    account_disc: str
    bsClass: str
    debit_amount: float
    credit_amount: float
    user: str
    created: datetime

#=============================================SQL Alchemy================================================

class UserLogin(BaseModel):
    
    id: int
    fullname = str
    username = str
    password_admin = str
    admin_status = str
    



#==============================================Rizal=======================================================
class DieselConsumption(BaseModel):
   
    transaction_date: date
    equipment_id: str
    withdrawal_slip: str
    use_liter: float
    price: float
    amount: float
    username: str
    date_update: date






   
#===============================================Surigao Database==============================
class DollarBill(BaseModel):
    """This is for Dollar Bill Pydantic Model"""
    trans_date: date
    equipment_id: str
    trackFactor: float
    no_trips: float
    usd_pmt: float  
    convertion_rate: float
    taxRate: float
    vat_output: float
    user:str
    date_credited: date


class InsertPesoBill(BaseModel):
    """This is for Surigao Peso Bill Pydantic Model"""
    trans_date: date
    equipment_id: str
    ore_owner: str
    trackFactor: float
    no_trips: float
    distance: float
    rate: float
    taxRate: float
    vat_output: float
    date_credited: date
    user: str
   

class Cashadvance(BaseModel):
    """This is for cash advance Pydantic Model"""

    employee_id : str
    lastname: str
    firstname: str
    ca_deduction:float


class SgmcEquipment(BaseModel):
    """This is for equipmenti Pydantic model for SGMC"""

    equipment_id: str 
    equipmentDiscription: str 
    rentalRate: float
    comments: str 
    owners: str 
    user: Optional[str]
    date_updated:  Optional[datetime] 
    date_credited: Optional[datetime] 

class RentalSgmc(BaseModel):
    """This is for SGMC Rental Equipment model"""
    transDate: date
    eur: str 
    equipment_id: str 
    timeIn: float
    timeOut: float
    totalHours: float
    rentalRate: float
    amount: float
    shift: str 
    driver_operator: str 
    user: Optional[str]
    date_updated:  Optional[datetime]
    date_credited: Optional[datetime]

class DieselSGMC(BaseModel):
    transDate: date
    withdrawal_slip: str
    equipment_id: Optional[int] 
    literUse: float
    price: float
    amount: float
    user: Optional[str]
    date_updated:  Optional[datetime]
    date_credited: Optional[datetime]
class CostSGMC_model(BaseModel):
    transDate: date
    equipment_id: Optional[int]
    cost_details: str 
    amount: float
    particular: str 
    user: Optional[str]
    date_updated:  Optional[datetime]
    date_created: Optional[datetime]


# ==========================================Zamboanga Table============================================

class Equipment(BaseModel):
    """This is for inserting Zamboanga Equipment true Pydatic Model"""

    equipment_id: str
    equipment_desc: str
    remarks: str

class Routes(BaseModel):
    """This is for inserting Routes Zamboanga Vitali Project"""
    routes_name: str
    distance: float

class Hauling(BaseModel):
    """This is for Pydantic Hauling Zamboanga Vitali Project"""
    trans_date: date
    equipment_id: str
    routes: str
    distance: float
    trackFactor: float
    no_trips: float
    volume: float
    rate: float
    taxRate: float
    amount: float
    vat_output: float
    net_of_vat: float
    user: str
    # date_updated: date
    # date_credited: date

class Vitalidiesel(BaseModel):
    """This is for Pydantic Diesel Zamboanga Vitali Project"""
    trans_date: date
    equipment_id: str
    withdrawal_slip: str
    liters: float
    price: float
    amount: float
    user: str


#==============================================TVI Project Model=============================================
class tviEquipment(BaseModel):
    """This is for inserting TVI Equipment true Pydatic Model"""

    equipmentId: str
    equipmentDesc: str
    rentalRate: float
    remarks: str
    owner: str


class tviRentalTrans(BaseModel):
    """This is for inserting TVI Rental Transaction true Pydatic Model"""

    transDate: date
    equipmentId: str
    totalHours: float
    rentalRate: float
    taxRate: float
    vat_output: float
    driverOperator: str
    owner: str

class TVIRentalTransaction(BaseModel):
    transDate: date
    demr: str
    equipmentId: str
    totalHours: float
    rentalRate: float
    totalAmount: float
    taxRate: float
    vat_output: float
    net_of_vat: float
    project_site: str
    driverOperator: str
    


class TVIDiesel(BaseModel):
    transDate: date
    equipmentId: str
    withdrawalSlip: str
    totalliters: float
    price: float
    totalAmount: float
    
#===========================================Rizal Equipment=======================================
class EquipmentDetails(BaseModel):
    """This is for  Equipment """
    equipment_id: str
    purchase_date: date
    description: str
    purchase_amount: float
    rental_rate: float
    plate_number: str
    status: str
    owner: str  
    
#=========================================Employee Frame==========================================
class EmployeeReg(BaseModel):
    """This is for employee regsitration"""
    
    lastName: str
    firstName: str
    middleName: str
    gender: str
    address_employee: str
    contactNumber: str
    contact_person: str
    emer_cont_person: str
    position: str
    date_hired: date
    department: str
    end_contract: str
    tin: str
    sssNumber: str
    phicNumber: str
    hdmfNumber: str
    employment_status: str
    salary_rate: float
    taxCode: str
    off_on_details: str
    Salary_Detail: str


class EmployeeReg2(BaseModel):
    """This is for employee regsitration"""
    employee_id: str
    lastName: str
    firstName: str
    middleName: str
    gender: str
    address_employee: str
    contactNumber: str
    contact_person: str
    emer_cont_person: str
    position: str
    date_hired: date
    department: str
    end_contract: str
    tin: str
    sssNumber: str
    phicNumber: str
    hdmfNumber: str
    employment_status: str
    salary_rate: float
    taxCode: str
    off_on_details: str
    Salary_Detail: str

class RizalRental(BaseModel):
    """This is for employee transaction Inserting Rental"""

    transaction_date: date
    equipment_id:  str 
    total_rental_hour: float
    rental_rate: float
    rental_amount: float
    eur_form: str

class RizalDiesel(BaseModel):
    """This is for employee transaction Inserting Diesel"""
    transaction_date: date
    equipment_id: str 
    withdrawal_slip: str 
    use_liter: float
    price: float
    amount: float
    


class RizalTonnagehaul(BaseModel):
    """This is for Tonnage Hauling in Rizal Model"""
    transDate: date
    equipment_id: str
    tripTicket: str
    totalTrip: float
    totalTonnage: float
    rate: float
    amount: float
    driverOperator: str


class Cost(BaseModel): 
    """This is for cost or expenses table"""
   
    transDate: date
    equipment_id: str 
    salaries: float
    fuel: float
    oil_lubes: float
    mechanicalSupplies: float
    repairMaintenance: float
    meals: float
    transpo: float
    tires: float
    amortization: float
    others: float
    totalAmount: float



class TVIRentalTransactionEmployeeLogin(BaseModel):
    transDate: date
    demr: str
    equipmentId: str
    time_in: datetime
    time_out: datetime
    totalHours: float
    rentalRate: float
    totalAmount: float
    taxRate: float
    vat_output: float
    net_of_vat: float
    project_site: str
    driverOperator: str


class TVIRoutes(BaseModel):
    routes: str
    distance: float
    
class TVITons(BaseModel):
    transDate: date
    equipmentId: str
    tripTicket: str
    routes: str
    trips: float 
    volume_tons: float
    distance: float 
    hauling_rate: float
    project_site: str
    driverOperator: str

class TVIPayroll(BaseModel):
    transDate: date
    employee_id: str 
    first_name: str 
    last_name: str 
    salaryRate: float
    addOnRate:  float
    salaryDetails: Optional[str]
    regDay: float
    regDayOt: float
    sunday: float
    sundayOT: float
    spl: float
    splOT: float
    lgl2: float
    lgl2OT: float
    lgl1: float
    nightDiff: float
    adjustment: float
    date_updated: Optional[datetime]
    date_credited: Optional[datetime]

class TviDiesel(BaseModel):
    """This is for employee transaction Inserting Diesel"""
    transDate: date
    equipmentId: str 
    withdrawalSlip: str 
    totalliters: float
    price: float
    totalAmount: float
    


class EquipmentGRC(BaseModel):
    equipment_id: str 
    equipmentDiscription: str 
    rentalRate: float
    comments: str 
    owners: str 
    user: Optional[str]
    date_updated:  Optional[datetime]
    date_credited: Optional[datetime]

class GrcRentalModels(BaseModel):
    transDate: date
    demr: str 
    equipment_id: str
    timeIn: Optional[datetime] 
    timeOut: Optional[datetime] 
    totalHours: float
    rentalRate: float
    amount: float
    shift: str 
    driver_operator: str 
    user: Optional[str]
    date_updated:  Optional[datetime] 
    date_credited: Optional[datetime]

class GrcDiesel(BaseModel):

    transDate: date
    withdrawal_slip: str 
    equipment_id: str
    literUse: float
    price: float
    amount: float
    user: Optional[str]
    date_updated:  Optional[datetime] 
    date_credited: Optional[datetime]


# developer transactions
class AccessSetting(BaseModel):

    user_id: str
    username: str
    accounting_write: bool
    accounting_read: bool
    payroll_write: bool
    payroll_read:bool
    site_transaction_write: bool
    site_transaction_read: bool
    date_updated:  Optional[datetime] 
    date_credited: Optional[datetime]
    inventory_write: bool
    inventory_read: bool


#============================================Inventory Transaction Frame=====================================
class InventoryItemsModel(BaseModel):
    item_name: str 
    description: str 
    category: str 
    uom: str 
    supplier: str 
    price: float
    quantity_in_stock: float
    minimum_stock_level: float
    location: str 
    tax_code: str
    user: Optional[str]
    date_updated: Optional[datetime]
    date_credited: Optional[datetime]

class InventoryTransactionsModel(BaseModel):
    inventory_item_id: int 
    transaction_type: str 
    transaction_date: date
    quantity: float
    unit_price: float
    total_price: float
    mrs_no: str 
    si_no_or_withslip_no: str 
    end_user: str 
    user: Optional[str]
    date_updated: Optional[datetime]
    date_credited: Optional[datetime]

class InventoryTransactionsPerQuantityUpdate(BaseModel):
    inventory_item_id: Optional[int]
    transaction_type: Optional[str]
    quantity: float

class InventoryItem(BaseModel):
    inventory_item_id: int
    quantity: float
    unit_price: float
    total_price: float
    end_user: str


class InventoryTransactionsModel2(BaseModel):
    transaction_type: str
    transaction_date: str
    mrs_no: int
    si_no_or_withslip_no: int
    items: List[InventoryItem]


    