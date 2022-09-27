from dataclasses import dataclass
import mysql.connector
from pickle import NONE
from datetime import date


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

        # try: 
        #     cursor.execute(
        #         """CREATE TABLE IF NOT EXISTS peso_bill (id INT AUTO_INCREMENT PRIMARY KEY, 
        #                     trans_date date,
        #                     equipment_id VARCHAR(100),
        #                     ore_owner VARCHAR(100), 
        #                     trackFactor DECIMAL(9,2),
        #                     no_trips DECIMAL(9,2),
        #                     distance DECIMAL(9,2),
        #                     totalVolume DECIMAL(9,2) GENERATED ALWAYS AS (trackFactor*no_trips*distance) STORED,
        #                     rate DECIMAL(9,2),
        #                     php_amount DECIMAL(9,2) GENERATED ALWAYS AS (totalVolume*rate) STORED,
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
    def select_one_from_dollarBill(id):
        """This function is for querying to diesel Database with out parameters"""
        SurigaoDB.DATABASE._open_connection()
        try:
            data = 'SELECT * FROM dollar_bill \
                WHERE id LIKE %s'

            val = ('%' + id + '%',)
            cursor.execute(data,(val),)
            
            # data = ('SELECT FROM dollar_bill \
            #     WHERE id = "'+id+'"')       
                        
            # # cursor.execute(data)              
            # cursor.execute(data) 
            return cursor.fetchone()
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
            SurigaoDB.DATABASE.commit()
            SurigaoDB.DATABASE.close()


    @staticmethod
    def update_one_dollarBill(trans_date,equipment_id,trackFactor,\
                        no_trips,usd_pmt,convertion_rate,taxRate,\
                            vat_output,user,date_credited,id):
        """
        This function is to update Equipment with parameters of Trans ID
        """
        SurigaoDB.DATABASE._open_connection()
        
        try:
            data = ('UPDATE dollar_bill SET trans_date=%s, equipment_id=%s,\
                   trackFactor=%s,no_trips=%s, \
                     usd_pmt=%s,convertion_rate=%s,taxRate=%s,\
                       vat_output=%s, user=%s,date_credited=%s \
                        WHERE id = %s')
            val =(trans_date,equipment_id,trackFactor,no_trips,
                    usd_pmt,convertion_rate,taxRate,vat_output,
                    user,date_credited,id)
            cursor.execute(data,val)
           
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
            SurigaoDB.DATABASE.commit()
            SurigaoDB.DATABASE.close()
           


#===============================================Peso Bill =============================================

    @staticmethod
    def insert_peso_production(trans_date,equipment_id,ore_owner,trackFactor,
                                no_trips,distance,rate,taxRate,
                                vat_output,date_credited):
        """This is to insert to dollar_bill Table"""
        SurigaoDB.DATABASE._open_connection() # to open database connection

        try:
            
            data = ( "INSERT INTO peso_bill (trans_date,equipment_id,ore_owner,trackFactor,\
                                no_trips,distance,rate,taxRate,vat_output,date_credited)"
                    "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            val = (trans_date,equipment_id,ore_owner,trackFactor,no_trips,
                            distance,rate,taxRate,vat_output,date_credited)
            #                  
            # cursor.execute(data)              
            cursor.execute(data,val) 
            
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:

            SurigaoDB.DATABASE.commit()
            SurigaoDB.DATABASE.close()

    @staticmethod
    def select_all_from_peso():
        """This function is for querying to diesel Database with out parameters"""
        SurigaoDB.DATABASE._open_connection()
        try:
            data = ('SELECT * FROM peso_bill')

            cursor.execute(data)
            return cursor.fetchall()
        
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
           
            SurigaoDB.DATABASE.close()

    @staticmethod
    def delete_one_from_peso(id):
        """This function is for querying to diesel Database with out parameters"""
        SurigaoDB.DATABASE._open_connection()
        try:
            data = ('DELETE FROM peso_bill \
                WHERE id = "'+id+'"')       
                        
            # cursor.execute(data)              
            cursor.execute(data) 
        
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
            SurigaoDB.DATABASE.commit()
            SurigaoDB.DATABASE.close()

# ======================================== Equipment transaction===============================
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
            



    