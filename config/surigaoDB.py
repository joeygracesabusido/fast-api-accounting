from dataclasses import dataclass
import mysql.connector
from pickle import NONE


class SurigaoDB(object):
    
    DATABASE = NONE

    def initialize():

        SurigaoDB.DATABASE = mysql.connector.connect(
                                host="192.46.225.247",
                                user="joeysabusido",
                                password="Genesis@11",
                                database="ldsurigao",
                                auth_plugin='mysql_native_password')
        global cursor
        cursor = SurigaoDB.DATABASE.cursor()

        SurigaoDB.DATABASE._open_connection()

        # try: 
        #     cursor.execute(
        #         """CREATE TABLE IF NOT EXISTS dollar_bill (id INT AUTO_INCREMENT PRIMARY KEY, 
        #                     trans_date date,
        #                     equipment_id VARCHAR(100), 
        #                     trackFactor DECIMAL(9,2),
        #                     no_trips DECIMAL(9,2),
        #                     totalVolume DECIMAL(9,2) GENERATED ALWAYS AS (trackFactor*no_trips) STORED,
        #                     usd_pmt DECIMAL(9,2),
        #                     usd_totalAmount DECIMAL(9,2) GENERATED ALWAYS AS (totalVolume*usd_pmt) STORED,
        #                     convertion_rate DECIMAL(9,2),
        #                     php_amount DECIMAL(9,2) GENERATED ALWAYS AS (usd_totalAmount*convertion_rate) STORED,
        #                     taxRate DECIMAL(3,2),
        #                     vat_output DECIMAL(9,2),
        #                     net_of_vat DECIMAL(9,2) GENERATED ALWAYS AS (php_amount-vat_output) STORED,
        #                     user VARCHAR(100),
        #                     date_credited date) """)
                    
        # except Exception as ex:
        #     print("Error", f"Error due to :{str(ex)}")

        # finally:
        #     SurigaoDB.DATABASE.commit()
        #     SurigaoDB.DATABASE.close()
    
    @staticmethod
    def insert_production(trans_date,equipment_id,trackFactor,
                                no_trips,usd_pmt,convertion_rate,taxRate,
                                vat_output,date_credited):
        """This is to insert to dollar_bill Table"""
        SurigaoDB.DATABASE._open_connection() # to open database connection

        try:
           
            data = ( "INSERT INTO dollar_bill (trans_date,equipment_id,trackFactor,\
                                no_trips,usd_pmt,convertion_rate,taxRate,vat_output,date_credited)"
                    "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            val = (trans_date,equipment_id,trackFactor,no_trips,
                            usd_pmt,convertion_rate,taxRate,vat_output,date_credited)
            #                  
            # cursor.execute(data)              
            cursor.execute(data,val) 
           
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:

            SurigaoDB.DATABASE.commit()
            SurigaoDB.DATABASE.close()


    @staticmethod
    def select_all_from_dollarBill():
        """This function is for querying to diesel Database with out parameters"""
        SurigaoDB.DATABASE._open_connection()
        try:
            data = ('SELECT * FROM dollar_bill')

            cursor.execute(data)
            return cursor.fetchall()
        
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
           
            SurigaoDB.DATABASE.close()


    @staticmethod
    def select_all_equipment():
        """This function is for querying to diesel Database with out parameters"""
        SurigaoDB.DATABASE._open_connection()
        try:
            data = ('SELECT * FROM equipment')

            cursor.execute(data)
            return cursor.fetchall()
        
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
           
            SurigaoDB.DATABASE.close()