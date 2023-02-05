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

        # try: 
        #     cursor.execute(
        #         """CREATE TABLE IF NOT EXISTS fund_request (id INT AUTO_INCREMENT PRIMARY KEY, 
        #                     transDate date,
        #                     payee VARCHAR (100) NOT NULL, 
        #                     particular VARCHAR (300) ,
        #                     amount DECIMAL(9,2),
        #                     user VARCHAR(100),
        #                     date_updated date,
        #                     date_credited DATETIME) """)
                    
        # except Exception as ex:
        #     print("Error", f"Error due to :{str(ex)}")

        # finally:
        #     Database.DATABASE.commit()
        #     Database.DATABASE.close()


        # try: 
        #     cursor.execute(
        #         """CREATE TABLE IF NOT EXISTS hauling_tonnage (id INT AUTO_INCREMENT PRIMARY KEY, 
        #                     transDate date,
        #                     equipment_id VARCHAR (100) NOT NULL, 
        #                     tripTicket  VARCHAR (100) ,
        #                     totalTrip DECIMAL(9,2),
        #                     totalTonnage DECIMAL(9,2),
        #                     rate DECIMAL(9,2),
        #                     amount DECIMAL(9,2),
        #                     driverOperator VARCHAR (100) , 
        #                     user VARCHAR(100),
        #                     date_updated DATETIME,
        #                     date_credited DATETIME) """)
                    
        # except Exception as ex:
        #     print("Error", f"Error due to :{str(ex)}")

        # finally:
        #     Database.DATABASE.commit()
        #     Database.DATABASE.close()

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
    def select_allEquipment_autocomplete(equipment_id):
        """
        This function is for querying for Equipment
        """

       
        Database.DATABASE._open_connection()
        try:
            data = ('SELECT * FROM equipment_details WHERE equipment_id like  "%'+equipment_id+'%" ORDER BY equipment_id')

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


    @staticmethod
    def updateEmployeeDetails(id,lastName,firstName, middleName, gender,  #5
                            address_employee,contactNumber,contact_person,emer_cont_person,position, # 5
                            date_hired,department,end_contract,tin,sssNumber,phicNumber, # 6
                            hdmfNumber,employment_status,salary_rate,taxCode,off_on_details,Salary_Detail,user, # 6
                            update_date):
        """
        This function is to update Equipment with parameters of ID
        """
        # Use the `with` statement to handle opening and closing the database connection
        # with TviDB.DATABASE:
        Database.DATABASE._open_connection()
        cursor = Database.DATABASE.cursor()
        with Database.DATABASE:
            try:
                # Use a parameterized query to prevent SQL injection attacks
                update_query = '''
                    UPDATE employee_details
                    SET  lastName=%s,firstName=%s, middleName=%s, gender=%s,
                            address_employee=%s,contactNumber=%s,contact_person=%s,emer_cont_person=%s,position=%s,
                            date_hired=%s,department=%s,end_contract=%s,tin=%s,sssNumber=%s,phicNumber=%s,
                            hdmfNumber=%s,employment_status=%s,salary_rate=%s,taxCode=%s,off_on_details=%s,Salary_Detail=%s,
                            user=%s,update_date=%s
                    WHERE id = %s
                '''
                cursor.execute(update_query, (lastName,firstName, middleName, gender, #4
                            address_employee,contactNumber,contact_person,emer_cont_person,position, #5
                            date_hired,department,end_contract,tin,sssNumber,phicNumber, #6
                            hdmfNumber,employment_status,salary_rate,taxCode,off_on_details,Salary_Detail, # 6
                            user,update_date,id)) # 2
                Database.DATABASE.commit() 
                # TviDB.DATABASE.close()
            except Exception as ex:
                print("Error", f"Error due to :{str(ex)}")

    @staticmethod
    def get_employeeDepartment(department):
        """This function is for Employee List by department"""

        # Use a with statement to automatically manage the database connection
        Database.DATABASE._open_connection()
        try:
            
            query = ('SELECT employee_id, lastName, firstName,position,department,off_on_details,employment_status\
                FROM employee_details\
                WHERE department LIKE "%'+department+'%" ORDER BY lastName\
                 ')
                
            

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
    def get_totalNumberEmployee(department):
        """This function is for Employee List by department"""

        # Use a with statement to automatically manage the database connection
        Database.DATABASE._open_connection()
        try:
            
            query = 'SELECT COUNT(employee_id) \
                FROM employee_details \
                WHERE department LIKE "%'+department+'%" AND off_on_details ="on" AND employment_status ="Employeed" \
                     ORDER BY lastName\
                 '
                
            

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
    def get_totalNumberEmployee_off(department):
        """This function is for Employee List by department"""

        # Use a with statement to automatically manage the database connection
        Database.DATABASE._open_connection()
        try:
            
            query = 'SELECT COUNT(employee_id) \
                FROM employee_details \
                WHERE department LIKE "%'+department+'%" AND off_on_details ="off" AND employment_status ="Employeed" \
                     ORDER BY lastName\
                 '
                
            

            # Execute the query
            cursor.execute(query)

            # Return the results of the query
            return cursor.fetchall()

        except Exception as ex:
            # Handle any errors that may occur
            print("Error", f"Error due to: {ex}")

        finally:
            
            Database.DATABASE.close()


#=================================================Rizal Tonnage ===========================================
    @staticmethod
    def insertTonnagehauling(transDate,equipment_id,tripTicket,totalTrip,totalTonnage, 
                            rate,amount,driverOperator,user,date_credited):
        """This function is for inserting Data to Cash advances"""
        Database.DATABASE._open_connection()
        try:
            data =  ("INSERT INTO hauling_tonnage (transDate,equipment_id,tripTicket,totalTrip, \
    totalTonnage,rate,amount,driverOperator,user,date_credited)"
                "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")   
            val = (transDate,equipment_id,tripTicket,totalTrip,totalTonnage, 
                            rate,amount,driverOperator,user,date_credited)       
            # cursor.execute(data)              
            cursor.execute(data,val) 
        
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
            Database.DATABASE.commit()
            Database.DATABASE.close() 

    


    @staticmethod
    def get_tonnageHaul(datefrom,dateto,equipment_id):
        """This function is for querying hauling tons transaction using Date and Equipment ID"""

        # Use a with statement to automatically manage the database connection
        Database.DATABASE._open_connection()
        try:
            
            query = ('SELECT * FROM hauling_tonnage \
                WHERE transDate BETWEEN "' + datefrom + '" AND  "' + dateto + '" AND  \
                equipment_id  like  "%'+equipment_id+'%" ORDER BY transDate\
                 ')
                
            

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
    def get_tonnageHaulID(id):
        """This function is for hauling Tonnage Transaction"""

        # Use a with statement to automatically manage the database connection
        Database.DATABASE._open_connection()
        try:
            
            query = ('SELECT * FROM hauling_tonnage \
                WHERE id like "%'+id+'%" \
                 ')
                
            

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
    def updateTonnageRizal(transDate,equipment_id,tripTicket,totalTrip,totalTonnage, 
                            rate,amount,driverOperator,user,date_updated,id):
        """
        This function is to update Tonnage with parameters of ID
        """
        # Use the `with` statement to handle opening and closing the database connection
        # with TviDB.DATABASE:
        Database.DATABASE._open_connection()
        cursor = Database.DATABASE.cursor()
        with Database.DATABASE:
            try:
                # Use a parameterized query to prevent SQL injection attacks
                update_query = '''
                    UPDATE hauling_tonnage
                    SET  transDate=%s,equipment_id=%s, tripTicket=%s, totalTrip=%s,
                            totalTonnage=%s,rate=%s,amount=%s,driverOperator=%s,user=%s,
                            date_updated=%s
                    WHERE id = %s
                '''
                cursor.execute(update_query, (transDate,equipment_id,tripTicket,totalTrip,totalTonnage, 
                            rate,amount,driverOperator,user,date_updated,id)) # 2
                Database.DATABASE.commit() 
                Database.DATABASE.close()
            except Exception as ex:
                print("Error", f"Error due to :{str(ex)}")


    @staticmethod
    def get_ton_cost(datefrom,dateto):
        """This function is for querying hauling tons transaction using Date and Equipment ID"""

        # Use a with statement to automatically manage the database connection
        Database.DATABASE._open_connection()
        try:
            
            query = ('SELECT transDate, equipment_id, \
                sum(totalTrip)  as totalTrip, \
                sum(totalTonnage)  as totalTons, \
                sum(amount)  as totalAmount\
                 FROM hauling_tonnage \
                WHERE transDate BETWEEN "' + datefrom + '" AND  "' + dateto + '"   \
                GROUP BY transDate ,equipment_id \
                 ORDER BY transDate ')
                
            

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
    def get_rental_cost(datefrom,dateto):
        """This function is for querying hauling tons transaction using Date and Equipment ID"""

        # Use a with statement to automatically manage the database connection
        Database.DATABASE._open_connection()
        try:
            
            query = ('SELECT  transaction_date, equipment_id, \
                sum(total_rental_hour)  as totalHours,\
                sum(rental_amount)  as totalAmount    \
                FROM  equipment_rental  \
                WHERE transaction_date BETWEEN "' + datefrom + '" AND  "' + dateto + '" \
                GROUP BY transaction_date ,equipment_id \
                ORDER BY transaction_date')
                
            

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
    def get_diesel_cost(datefrom,dateto):
        """This function is for querying Diesel transaction using Date and Equipment ID"""

        # Use a with statement to automatically manage the database connection
        Database.DATABASE._open_connection()
        try:
            
            query = ('SELECT equipment_id, \
                sum(use_liter)  as liters,\
                sum(amount)  as totalAmount    \
                FROM  diesel_consumption  \
                WHERE transaction_date BETWEEN "' + datefrom + '" AND  "' + dateto + '" \
                GROUP BY equipment_id \
                ORDER BY equipment_id')
                
            

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
    def get_costAnalysis(datefrom,dateto):
        """This function is for querying hauling tons transaction using Date and Equipment ID"""

        # Use a with statement to automatically manage the database connection
        Database.DATABASE._open_connection()
        try:
            
            query = ('SELECT c.equipment_id, \
                    CASE \
                            WHEN totalTonAmount IS NULL THEN 0 \
                            WHEN totalTonAmount IS NOT NULL THEN totalTonAmount \
                        \
                        END AS TonAmount,\
                            \
                        CASE \
                            WHEN TotalRentalAmount IS NULL THEN 0 \
                            WHEN TotalRentalAmount IS NOT NULL THEN TotalRentalAmount \
                        \
                        END AS RentalAmount,\
                        CASE \
                            WHEN totalDCamount IS NULL THEN 0 \
                            WHEN totalDCamount IS NOT NULL THEN totalDCamount \
                        \
                        END AS DieselAmount\
                    \
                    FROM (SELECT ht.equipment_id, ht.totalTonAmount, er.TotalRentalAmount \
                    FROM ( \
                    SELECT equipment_id, sum(amount) as totalTonAmount \
                    FROM hauling_tonnage \
                    WHERE transDate BETWEEN  "' + datefrom + '" AND "' + dateto + '" \
                    GROUP BY equipment_id \
                    ) ht \
                    LEFT JOIN ( \
                    SELECT equipment_id, sum(rental_amount) as TotalRentalAmount \
                    FROM equipment_rental \
                    WHERE transaction_date BETWEEN  "' + datefrom + '" AND "' + dateto + '" \
                    GROUP BY equipment_id \
                    ) er USING (equipment_id) \
                        \
                    UNION \
                            \
                    SELECT er.equipment_id, ht.totalTonAmount, er.TotalRentalAmount \
                    FROM ( \
                    SELECT equipment_id, sum(amount) as totalTonAmount \
                    FROM hauling_tonnage \
                    WHERE transDate BETWEEN  "' + datefrom + '" AND "' + dateto + '" \
                    GROUP BY equipment_id \
                    ) ht \
                    RIGHT  JOIN ( \
                    SELECT equipment_id, sum(rental_amount) as TotalRentalAmount \
                    FROM equipment_rental \
                    WHERE transaction_date BETWEEN  "' + datefrom + '" AND "' + dateto + '" \
                    GROUP BY equipment_id \
                    ) er USING (equipment_id) \
                    ) ab \
                    RIGHT  JOIN (SELECT dc.equipment_id , \
                    sum(dc.amount)as totalDCamount from diesel_consumption as dc \
                    WHERE dc.transaction_date BETWEEN  "' + datefrom + '" AND "' + dateto + '" \
                    GROUP BY dc.equipment_id)c ON c.equipment_id = ab.equipment_id \
                                    ')
                
            

            # Execute the query
            cursor.execute(query)

            # Return the results of the query
            return cursor.fetchall()

        except Exception as ex:
            # Handle any errors that may occur
            print("Error", f"Error due to: {ex}")

        finally:
            
            Database.DATABASE.close()



                




        

       

