from datetime import datetime
def chartofAccount(item) -> dict:
    return {
        "id": str(item["_id"]),
        "accountNum": str(item["accountNum"]),
        "accountTitle": str(item["accountTitle"]),
        "bsClass": str(item["bsClass"]),
        "user": str(item["user"]),
        "created": str(item["created"])
    }

def chartofAccounts(entity) -> list:
    return [chartofAccount(item) for item in entity] 