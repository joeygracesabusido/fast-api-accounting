from dataclasses import dataclass
import mysql.connector
from pickle import NONE
from datetime import date


class TviDB(object):
    
    DATABASE = NONE

    def initialize():

        TviDB.DATABASE = mysql.connector.connect(
                                host="192.46.225.247",
                                user="joeysabusido",
                                password="Genesis@11",
                                database="ldTviDB",
                                auth_plugin='mysql_native_password')
        global cursor
        cursor = TviDB.DATABASE.cursor()

        TviDB.DATABASE._open_connection()

        # try:
        #     cursor.execute(
        #         "CREATE TABLE IF NOT EXISTS equipment (id INT PRIMARY KEY AUTO_INCREMENT, \
        #                                 equipmentID VARCHAR(100), \
        #                                 equipmentDesc VARCHAR(100), \
        #                                 rentalRate DECIMAL(9,2), \
        #                                 remarks VARCHAR(200),\
        #                                 UNIQUE (equipmentID))"
        #     )
        # except Exception as ex:
        #     print("Error", f"Error due to :{str(ex)}")

        # finally:
        #     TviDB.DATABASE.commit()
        #     TviDB.DATABASE.close()