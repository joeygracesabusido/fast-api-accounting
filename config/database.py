from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# from sqlalchemy import *
import mysql.connector
import sqlalchemy
import databases

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://host:192.46.225.247,user:joeysabusido, \
#                                 password:Genesis@11/ldglobal"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()
# host="192.46.225.247",
# user="joeysabusido",
# password="Genesis@11",
# database="ldglobal",



# engine = create_engine("mysql+pymysql://host:192.46.225.247,user:joeysabusido,password:Genesis@11/ldglobal")

# meta = MetaData()
# con=engine.connect()

# sql_database_url="mysql+pymysql://host:192.46.225.247,user:joeysabusido,password:Genesis@11/ldgsurigao"

# engine=create_engine(sql_database_url)

# meta = MetaData()
# con=engine.connect()
# sessionLocal=sessionmaker(autocommit=False,bind=engine)

# Base=declarative_base()


# DATABASE_URL="mysql+pymysql://host:'192.46.225.247',\
#                 user:'joeysabusido',\
#                 password:'Genesis@11'/ldsurigao"

# mydb =  mysql.connector.connect(
#             host="192.46.225.247",
#             user="joeysabusido",
#             password="Genesis@11",
#             database="ldglobal",
#             auth_plugin='mysql_native_password')
# cursor = mydb.cursor()

# DATABASE_URL = "mysql+mysqlconnector://192.46.225.247:'3306',password:/Genesis@11,user:/joeysabusido/ldglobal"
               


# database = databases.Database(DATABASE_URL)
# metadata = sqlalchemy.MetaData()

# engine = sqlalchemy.create_engine(
#     DATABASE_URL
# )
# metadata.create_all(engine)


# import mysql.connector
# import logging as logger
# class Database:
#     __instance = None
#     def __init__(self):
#         if self.__instance is None or self.__instance.is_connected() == False:
#             self.__instance = mysql.connector.connect(
#               host="192.46.225.247",
#                 user="joeysabusido",
#                 password="Genesis@11",
#                 database="ldglobal",
#             )
#             self.__instance.autocommit = False
#     def query(self, query, autoCommit=None, fetch="ALL"):
#         try:
#             cursor = self.__instance.cursor()
#             result = cursor.execute(query)
#             if autoCommit is not None:
#                 self.__instance.commit()
#                 operation = True if cursor.lastrowid == 0 else {"id": cursor.lastrowid}
#                 return {"result": operation}
#             fields = [field_md[0] for field_md in cursor.description]
#             if fetch != "SINGLE":
#                 result = [dict(zip(fields, row)) for row in cursor.fetchall()]
#                 return {"result": result}
#             else:
#                 result = [dict(zip(fields, row)) for row in cursor.fetchone()]
#                 return {"result": result}
#         except Exception as e:
#             return {"result": None, "error": e, "query": query}
#             logger.error(e)
#         finally:
#             if self.__instance.is_connected():
#                 logger.info("Mantendo conexão.")
#                 # self.__instance.cursor.close()
#                 # self.__instance.close()
#                 # logger.debug("Removendo instancia da Database... OK")

from dataclasses import dataclass
import mysql.connector
from pickle import NONE

class Database(object):
    
    DATABASE = NONE

    def initialize():

        Database.DATABASE = mysql.connector.connect(
                                host="192.46.225.247",
                                user="joeysabusido",
                                password="Genesis@11",
                                database="ldglobal",
                                auth_plugin='mysql_native_password')
        global cursor
        cursor = Database.DATABASE.cursor()

        Database.DATABASE._open_connection()

        try: 
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS fund_request (id INT AUTO_INCREMENT PRIMARY KEY, 
                            transDate date,
                            payee VARCHAR (100) NOT NULL, 
                            particular VARCHAR (300) ,
                            amount DECIMAL(9,2),
                            user VARCHAR(100),
                            date_updated date,
                            date_credited DATETIME) """)
                    
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")

        finally:
            Database.DATABASE.commit()
            Database.DATABASE.close()

    @staticmethod
    def insert_diesel_consuption(transaction_date,equipment_id,withdrawal_slip,
                                use_liter,price,amount,username,date_update):
        """This is to insert to database Inventory and inventory_onhand Table"""
        Database.DATABASE._open_connection() # to open database connection

        try:
           
            data = ( "INSERT INTO diesel_consumption (transaction_date,equipment_id,\
                                withdrawal_slip,use_liter,price,amount,username,date_update)"
                    "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)")
            val = (transaction_date,equipment_id,withdrawal_slip,use_liter,
                            price,amount,username,date_update)
            #                  
            # cursor.execute(data)              
            cursor.execute(data,val) 
           
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:

            Database.DATABASE.commit()
            Database.DATABASE.close()

    @staticmethod
    def select_all_from_dieselDB():
        """This function is for querying to diesel Database with out parameters"""
        Database.DATABASE._open_connection()
        try:
            data = ('SELECT * FROM diesel_consumption')

            cursor.execute(data)
            return cursor.fetchall()
        
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
           
            Database.DATABASE.close()

    @staticmethod
    def select_diesel_withParams(datefrom,dateto):
        """This function is for querying diesel with Date parameters"""
        Database.DATABASE._open_connection()

        try:
            data = ("SELECT * FROM diesel_consumption \
                WHERE  transaction_date between '" + datefrom +"' AND '" + dateto +"'")

            # val = ('%' + id + '%',)
            cursor.execute(data)
            return cursor.fetchall()
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
            
            Database.DATABASE.close()

    @staticmethod
    def select_diesel_equipID(datefrom,dateto,equipment_id):
        """This function is for querying diesel with Date parameters"""
        Database.DATABASE._open_connection()

        try:
            data = ("SELECT * FROM diesel_consumption \
                WHERE  transaction_date between '" + datefrom +"' AND '" + dateto +"' AND equipment_id ='" + equipment_id +"' ")

            # val = ('%' + id + '%',)
            cursor.execute(data)
            return cursor.fetchall()
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
            
            Database.DATABASE.close()



    @staticmethod
    def select_dieselTrans(id):
        """
        This function is for querying with parameters of ID
        """
        Database.DATABASE._open_connection()
        try:
            data = 'SELECT * FROM diesel_consumption \
                WHERE id LIKE %s'

            val = ('%' + id + '%',)
            cursor.execute(data,(val),)
            return cursor.fetchone()
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
            
            Database.DATABASE.close()

    @staticmethod
    def update_one_diesel(transaction_date,equipment_id,withdrawal_slip,
                            use_liter,price,
                            amount,username,id):
        """
        This function is to update Equipment with parameters of Trans ID
        """
        Database.DATABASE._open_connection()
        try:
            data = ('UPDATE diesel_consumption SET transaction_date=%s, equipment_id=%s,\
                   withdrawal_slip=%s, \
                     use_liter=%s,price=%s,amount=%s,username=%s \
                        WHERE id = %s')
            val =(transaction_date,equipment_id,withdrawal_slip,use_liter,
                    price,amount,username,id)
            cursor.execute(data,val)
           
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
            Database.DATABASE.commit()
            Database.DATABASE.close()


# ===============================================Equipment Rental Transaction===========================
    @staticmethod
    def select_equipment(id):
        """
        This function is for querying with parameters of ID
        """

       
        Database.DATABASE._open_connection()
        try:
            data = ('SELECT * FROM equipment_details \
                WHERE equipment_id LIKE %s')

            val = ('%' + id + '%',)
            cursor.execute(data,(val),)
            return cursor.fetchall()
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
            # Database.DATABASE.commit()
            Database.DATABASE.close()

    @staticmethod
    def select_allEquipment():
        """
        This function is for querying for Equipment
        """

       
        Database.DATABASE._open_connection()
        try:
            data = ("SELECT * FROM equipment_details ORDER BY equipment_id")

            cursor.execute(data)
            return cursor.fetchall()
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
            # Database.DATABASE.commit()
            Database.DATABASE.close()
            

    @staticmethod
    def insert_rental_transaction(transaction_date,equipment_id,total_rental_hour,
                                rental_rate,rental_amount,username):
        """This is to insert to database rental to equipment_rental Table"""
        Database.DATABASE._open_connection() # to open database connection

        try:
           
            data = ( "INSERT INTO equipment_rental (transaction_date,equipment_id,total_rental_hour,\
                                rental_rate,rental_amount,username)"
                    "VALUES(%s,%s,%s,%s,%s,%s)")
            val = (transaction_date,equipment_id,total_rental_hour,rental_rate,
                            rental_amount,username)
            #                  
            # cursor.execute(data)              
            cursor.execute(data,val) 
           
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:

            Database.DATABASE.commit()
            Database.DATABASE.close()

    @staticmethod
    def select_all_from_rentalDB():
        """This function is for querying to diesel Database with out parameters"""
        Database.DATABASE._open_connection()
        try:
            data = ('SELECT * FROM equipment_rental ')

            cursor.execute(data)
            return cursor.fetchall()
        
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
           
            Database.DATABASE.close() 


    @staticmethod
    def select_rental_with_parameters(datefrom,dateto,equipment_id):
        """This function is for querying to diesel Database with out parameters"""
        Database.DATABASE._open_connection()
        try:
            data = 'SELECT * FROM equipment_rental WHERE transaction_date BETWEEN "' + datefrom +'" AND "' + dateto +'" \
                         AND  equipment_id like  "%'+equipment_id+'%" '

            cursor.execute(data)
            return cursor.fetchall()
        
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
           
            Database.DATABASE.close()   


    @staticmethod
    def delete_rental(id):
        """This function si for deleting Rental with Parametes"""
        Database.DATABASE._open_connection()    

        try:
            data = ('DELETE FROM equipment_rental \
                WHERE id = "'+id+'"')       
                        
            # cursor.execute(data)              
            cursor.execute(data) 
        
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
            Database.DATABASE.commit()
            Database.DATABASE.close()   





    
#=====================================Cash Advances==================================

    @staticmethod
    def insert_cash_advance(employee_id,lastname,firstname,ca_deduction):
        """This function is for inserting Data to Cash advances"""
        Database.DATABASE._open_connection()
        try:
            data =  ("INSERT INTO cash_advance (employee_id,lastname,firstname,ca_deduction)"
                "VALUES(%s,%s,%s,%s)")   
            val = (employee_id,lastname,firstname,ca_deduction)       
            # cursor.execute(data)              
            cursor.execute(data,val) 
        
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
            Database.DATABASE.commit()
            Database.DATABASE.close() 

    @staticmethod
    def select_all_cashAdvanves():
        """This function is for Querying Cash Advacnes"""

        Database.DATABASE._open_connection()
        try:
            data = ("SELECT * FROM cash_advance")

            cursor.execute(data)
            return cursor.fetchall()
        
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
           
            Database.DATABASE.close()   

   

    @staticmethod
    def delete_one_from_cash(id):
        """This function is for querying to diesel Database with out parameters"""
        Database.DATABASE._open_connection()
        try:
            data = ('DELETE FROM cash_advance \
                WHERE id = "'+id+'"')       
                        
            # cursor.execute(data)              
            cursor.execute(data) 
        
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
            Database.DATABASE.commit()
            Database.DATABASE.close()    

#===============================================Employee Details ==============================================
 
    @staticmethod
    def select_one_employee(firstName):
        """This function is for Querying Cash Advacnes"""

        Database.DATABASE._open_connection()
        try:
            data = ' select * from employee_details where firstName like  "%'+firstName+'%"'

            cursor.execute(data)
            return cursor.fetchall()
        
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
           
            Database.DATABASE.close()  

    @staticmethod
    def select_one_employee_with_empID(employee_id):
        """This function is for Querying Cash Advacnes"""

        Database.DATABASE._open_connection()
        try:
            data = ' select * from employee_details where employee_id like  "%'+employee_id+'%"'

            cursor.execute(data)
            return cursor.fetchall()
        
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
           
            Database.DATABASE.close() 


#======================================Rizal Payroll ======================================
    @staticmethod
    def computation13thMonth(date1,date2,department):
        """This function is for Querying Cash Advacnes"""

        Database.DATABASE._open_connection()
        try:
            data = ("SELECT employee_id,last_name,\
                sum(regularday_cal)  as TotalRegday,\
                sum(regularsunday_cal) / 1.30  as TotalRegSun,\
                sum(spl_cal) / 1.30 as TotalSpl,\
                sum(legal_day_cal) / 2 as Totallgl2,\
                sum(shoprate_day_cal)  as Totalshoprate,\
                sum(proviRate_day_cal)  as TotalproviRate,\
                sum(provisun_day_cal)/1.30  as TotalproviSun,\
                first_name, department \
            from payroll_computation \
            WHERE cut_off_date BETWEEN '" + date1 +"'AND '" + date2 +"' AND department LIKE '%" + department +"%' \
            GROUP BY employee_id ,last_name,first_name,department \
            ORDER BY last_name")
            
            cursor.execute(data)
            return cursor.fetchall()


        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
           
            Database.DATABASE.close() 


    @staticmethod
    def get_employee_cutoff_range(employee_id):
        """This function is for Querying for How Many cut off for Employee"""

        # Use a with statement to automatically manage the database connection
        Database.DATABASE._open_connection()
        try:
            
            query = ("SELECT cut_off_date, employee_id, last_name, first_name, grosspay_save, netpay_save,department \
                FROM payroll_computation\
                WHERE employee_id='" + employee_id +"' \
                ORDER BY cut_off_date ")
                
          

            # Execute the query
            cursor.execute(query)

            # Return the results of the query
            return cursor.fetchall()

        except Exception as ex:
            # Handle any errors that may occur
            print("Error", f"Error due to: {ex}")

        finally:
           
            Database.DATABASE.close()


    @staticmethod
    def get_employee_info(employee_id):
        """This function is for Querying for How Many cut off for Employee"""

        # Use a with statement to automatically manage the database connection
        Database.DATABASE._open_connection()
        try:
            
            # query = ("SELECT employee_id, lastName, firstName, middleName, gender,\
            #     address_employee,contactNumber,contact_person,emer_cont_person,position,\
            #         date_hired,department,end_contract,tin,sssNumber,phicNumber,hdmfNumber,employment_status\
            #             update_contract,salary_rate,taxCode,Salary_Detail \
            query = ("SELECT * \
                FROM employee_details\
                WHERE employee_id='" + employee_id +"' \
                 ")
                
            

            # Execute the query
            cursor.execute(query)

            # Return the results of the query
            return cursor.fetchall()

        except Exception as ex:
            # Handle any errors that may occur
            print("Error", f"Error due to: {ex}")

        finally:
            
            Database.DATABASE.close()


       

