from dataclasses import dataclass
import mysql.connector
from pickle import NONE
from datetime import date


class ZamboangaDB(object):
    
    DATABASE = NONE

    def initialize():

        ZamboangaDB.DATABASE = mysql.connector.connect(
                                host="192.46.225.247",
                                user="joeysabusido",
                                password="Genesis@11",
                                database="ldzamboanga",
                                auth_plugin='mysql_native_password')
        global cursor
        cursor = ZamboangaDB.DATABASE.cursor()

        ZamboangaDB.DATABASE._open_connection()

        # try: 
        #     cursor.execute(
        #         """CREATE TABLE IF NOT EXISTS routes (id INT AUTO_INCREMENT PRIMARY KEY, 
        #                     routes_name VARCHAR(100), 
        #                     distance DECIMAL(9,2),
        #                     date_credited date) """)
                    
        # except Exception as ex:
        #     print("Error", f"Error due to :{str(ex)}")

        # finally:
        #     ZamboangaDB.DATABASE.commit()
        #     ZamboangaDB.DATABASE.close()

        # try: 
        #     cursor.execute(
        #         """CREATE TABLE IF NOT EXISTS peso_bill (id INT AUTO_INCREMENT PRIMARY KEY, 
        #                     trans_date date,
        #                     routes VARCHAR(100),
        #                     distance DECIMAL(9,2), 
        #                     trackFactor DECIMAL(9,2),
        #                     no_trips DECIMAL(9,2),
        #                     distance DECIMAL(9,2),
        #                     rate DECIMAL(9,2),
        #                     taxRate DECIMAL(3,2),
        #                     vat_output DECIMAL(9,2),
        #                     net_of_vat DECIMAL(9,2) 
        #                     user VARCHAR(100),
        #                     date_credited date) """)
                    
        # except Exception as ex:
        #     print("Error", f"Error due to :{str(ex)}")

        # finally:
        #     ZamboangaDB.DATABASE.commit()
        #     ZamboangaDB.DATABASE.close()

