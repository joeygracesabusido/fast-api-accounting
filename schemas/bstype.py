from bson import ObjectId

def bsType(item) -> dict:
    return {
        "id": str(item["_id"]),
        "bstype": str(item["bstype"]),
       
    }

def bsTypes(entity) -> list:
    return [bsType(item) for item in entity] 