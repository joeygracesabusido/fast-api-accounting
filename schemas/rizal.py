from datetime import datetime, date
#===================================================Diesel Consuption========================================
def DieselConsumption(item) -> dict:
    return {
        "id": str(item[0]),
        "transaction_date": str(item[1]),
        
        "equipment_id": str(item[2]),
        "withdrawal_slip": str(item[3]),
        "use_liter": str(item[4]),
        "price": float(item[5]),
        "amount": float(item[6]),
        "transID": str(item[7]),
        "username": str(item[8]),
    }

def DieselConsumptions(entity) -> list:
    return [DieselConsumption(item) for item in entity] 

#==============================================for Equipment Detail==============================
def Equipment(item) -> dict:
    return {
        "id": str(item[0]),
        "equipment_id": str(item[1]),
        "purchase_date": str(item[2]),
        "description": str(item[3]),
        "purchase_amount": str(item[4]),
        "rental_rate": float(item[5]),
        "plate_number": str(item[6]),
       
    }

def Equipments(entity) -> list:
    return [Equipment(item) for item in entity] 


def RentalList(item) -> dict:
    return {
        "id": str(item[0]),
        "transaction_date": str(item[2]),
        "equipment_id": str(item[3]),
        "total_rental_hour": float(item[4]),
        "rental_rate": float(item[5]),
        "rental_amount": float(item[6]),
        "username": str(item[7]),
        
       
    }

def RentalLists(entity) -> list:
    return [RentalList(item) for item in entity] 



def CashAdvance(item) -> dict:
    return {
        "id": str(item[0]),
        "employee_id": str(item[1]),
        "lastname": str(item[2]),
        "firstname": str(item[3]),
        "ca_deduction": float(item[4]),
         
    }

def CashAdvances(entity) -> list:
    return [CashAdvance(item) for item in entity] 



