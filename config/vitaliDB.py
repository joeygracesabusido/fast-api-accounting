from fastapi import FastAPI
from fastapi import APIRouter, Body, HTTPException, Depends, Request, Response, status
from mysql.connector import connect

vitali = APIRouter(include_in_schema=False)

# @vitali.on_event("startup")
# async def startup():
#     vitali.db_connection = connect(
#         host="192.46.225.247",
#         user="joeysabusido",
#         password="Genesis@11",
#         database="ldvitali",
#         auth_plugin='mysql_native_password'
        
#     )
@vitali.on_event("startup")
async def startup():
    with connect(
        host="192.46.225.247",
        user="joeysabusido",
        password="Genesis@11",
        database="ldvitali",
        auth_plugin="mysql_native_password",
    ) as connection:
        vitali.db_connection = connection

# @vitali.on_event("shutdown")
# async def shutdown():
#     await vitali.db_connection.disconnect()


@vitali.post("/create-table")
async def create_table(equipment: str):
    
    cursor = vitali.db_connection.cursor()
    cursor.execute(
        f"CREATE TABLE {equipment} (id INT PRIMARY KEY AUTO_INCREMENT, \
                                 equipment_id VARCHAR(100), \
                                equipment_desc VARCHAR(100), \
                                remarks VARCHAR(200),\
                                UNIQUE (equipment_id))"
    )
    vitali.db_connection.commit()
    return {'Messege': 'Table has been created'}
    




