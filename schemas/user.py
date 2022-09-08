from datetime import datetime
def userEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "fullname": str(item["fullname"]),
        "username": str(item["username"]),
        "password": str(item["password"]),
        "status": str(item["status"]),
        "created": str(item["created"])
    }

def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity] 