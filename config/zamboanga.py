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
        #         """CREATE TABLE IF NOT EXISTS equipment (id INT AUTO_INCREMENT PRIMARY KEY, 
        #                     equipment_id VARCHAR(100), 
        #                     equipment_desc VARCHAR(100),
        #                     remarks VARCHAR(200),
        #                     UNIQUE (equipment_id))""")
                    
        # except Exception as ex:
        #     print("Error", f"Error due to :{str(ex)}")

        # finally:
        #     ZamboangaDB.DATABASE.commit()
        #     ZamboangaDB.DATABASE.close()

        # try: 
        #     cursor.execute(
        #         """CREATE TABLE IF NOT EXISTS routes (id INT AUTO_INCREMENT PRIMARY KEY, 
        #                     routes_name VARCHAR(100), 
        #                     distance DECIMAL(9,2),
        #                     UNIQUE (routes_name))""")
                    
        # except Exception as ex:
        #     print("Error", f"Error due to :{str(ex)}")

        # finally:
        #     ZamboangaDB.DATABASE.commit()
        #     ZamboangaDB.DATABASE.close()

        # try: 
        #     cursor.execute(
        #         """CREATE TABLE IF NOT EXISTS hauling (id INT AUTO_INCREMENT PRIMARY KEY, 
        #                     trans_date date,
        #                     equipment_id VARCHAR(100),
        #                     routes VARCHAR(100),
        #                     distance DECIMAL(9,2), 
        #                     trackFactor DECIMAL(9,2),
        #                     no_trips DECIMAL(9,2),
        #                     volume DECIMAL(9,2),
        #                     rate DECIMAL(9,2),
        #                     taxRate DECIMAL(3,2),
        #                     amount DECIMAL(9,2),  
        #                     vat_output DECIMAL(9,2),
        #                     net_of_vat DECIMAL(9,2), 
        #                     user VARCHAR(100),
        #                     date_updated date,
        #                     date_credited date) """)
                    
        # except Exception as ex:
        #     print("Error", f"Error due to :{str(ex)}")

        # finally:
        #     ZamboangaDB.DATABASE.commit()
        #     ZamboangaDB.DATABASE.close()

    @staticmethod
    def select_all_equipment():
        """
        This function is for querying all equipment
        """

       
        ZamboangaDB.DATABASE._open_connection()
        try:
            data = ('SELECT * FROM equipment \
                ')

            cursor.execute(data)
            return cursor.fetchall()
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
            # Database.DATABASE.commit()
            ZamboangaDB.DATABASE.close()


    @staticmethod
    def select_equipment(id):
        """
        This function is for querying with parameters of ID
        """

       
        ZamboangaDB.DATABASE._open_connection()

        try:
            data = ' select * from equipment where id like  "%'+id+'%"'

            cursor.execute(data)
            return cursor.fetchall()
        
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
           
            ZamboangaDB.DATABASE.close()

       


    @staticmethod
    def insert_equipment(equipment_id,equipment_desc,remarks):
        """This is to insert to database rental to equipment_rental Table"""
        ZamboangaDB.DATABASE._open_connection() # to open database connection

        try:
           
            data = ( "INSERT INTO equipment (equipment_id,equipment_desc,remarks)"
                    "VALUES(%s,%s,%s)")
            val = (equipment_id,equipment_desc,remarks)
            #                  
            # cursor.execute(data)              
            cursor.execute(data,val) 
           
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:

            ZamboangaDB.DATABASE.commit()
            ZamboangaDB.DATABASE.close()


    @staticmethod
    def update_equipment(id,equipment_id,equipment_desc,remarks):
        """
        This function is to update Equipment with parameters of  ID
        """
        ZamboangaDB.DATABASE._open_connection()
        try:
            data = ('UPDATE equipment SET equipment_id=%s, equipment_desc=%s,\
                   remarks=%s\
                        WHERE id = %s')
            val =(equipment_id,equipment_desc,remarks,id)
            cursor.execute(data,val)
           
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
            ZamboangaDB.DATABASE.commit()
            ZamboangaDB.DATABASE.close()


    @staticmethod
    def delete_equipment(id):
        """This function si for deleting Rental with Parametes"""
        ZamboangaDB.DATABASE._open_connection()    

        try:
            data = ('DELETE FROM equipment \
                WHERE id = "'+id+'"')       
                        
            # cursor.execute(data)              
            cursor.execute(data) 
        
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
            ZamboangaDB.DATABASE.commit()
            ZamboangaDB.DATABASE.close()  


#==========================================Routes Frame=============================================

    # routes_name VARCHAR(100), 
    # distance DECIMAL(9,2),

    @staticmethod
    def select_all_routes():
        """
        This function is for querying all routes
        """

       
        ZamboangaDB.DATABASE._open_connection()
        try:
            data = ('SELECT * FROM routes \
                ')

            cursor.execute(data)
            return cursor.fetchall()
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
            # Database.DATABASE.commit()
            ZamboangaDB.DATABASE.close()
 
    @staticmethod
    def insert_routes(routes_name,distance):
        """This is to insert to database rental to equipment_rental Table"""
        ZamboangaDB.DATABASE._open_connection() # to open database connection

        try:
           
            data = ( "INSERT INTO routes (routes_name,distance)"
                    "VALUES(%s,%s)")
            val = (routes_name,distance)
            #                  
            # cursor.execute(data)              
            cursor.execute(data,val) 
           
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:

            ZamboangaDB.DATABASE.commit()
            ZamboangaDB.DATABASE.close()


    @staticmethod
    def delete_routes(id):
        """This function si for deleting Rental with Parametes"""
        ZamboangaDB.DATABASE._open_connection()    

        try:
            data = ('DELETE FROM routes \
                WHERE id = "'+id+'"')       
                        
            # cursor.execute(data)              
            cursor.execute(data) 
        
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
            ZamboangaDB.DATABASE.commit()
            ZamboangaDB.DATABASE.close()


    @staticmethod
    def select_routes(routes_name):
        """
        This function is for querying with parameters of ID
        """

       
        ZamboangaDB.DATABASE._open_connection()
        try:
            data = ('SELECT * FROM routes \
                WHERE routes_name LIKE %s')

            val = ('%' + routes_name + '%',)
            cursor.execute(data,(val),)
            return cursor.fetchall()
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
            # Database.DATABASE.commit()
            ZamboangaDB.DATABASE.close()  

#=========================================Vitali Hauling ===========================================
   

    @staticmethod
    def insert_hauling(trans_date,equipment_id,routes,
                        distance,trackFactor,no_trips,volume,
                        rate,taxRate,amount,vat_output,net_of_vat,user,date_credited):
        """This is to insert to database rental to hauling Table"""
        ZamboangaDB.DATABASE._open_connection() # to open database connection

        try:
           
            data = ( "INSERT INTO hauling (trans_date,equipment_id,routes,\
                        distance,trackFactor,no_trips,volume,\
                        rate,taxRate,amount,vat_output,net_of_vat,user,date_credited)"
                    "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            val = (trans_date,equipment_id,routes,
                        distance,trackFactor,no_trips,volume,
                        rate,taxRate,amount,vat_output,net_of_vat,user,date_credited)
            #                  
            # cursor.execute(data)              
            cursor.execute(data,val) 
           
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:

            ZamboangaDB.DATABASE.commit()
            ZamboangaDB.DATABASE.close()


    @staticmethod
    def select_all_hauling():
        """
        This function is for querying all hauling
        """

       
        ZamboangaDB.DATABASE._open_connection()
        try:
            data = ('SELECT * FROM hauling \
                ')

            cursor.execute(data)
            return cursor.fetchall()
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
            # Database.DATABASE.commit()
            ZamboangaDB.DATABASE.close()

    @staticmethod
    def select_hauling_withParams(equipment_id,datefrom,dateto):
        """
        This function is for querying with parameters of ID & Date
        """

       
        ZamboangaDB.DATABASE._open_connection()

        try:
            data = ' select * from hauling where \
                         trans_date BETWEEN "'+datefrom+'" AND "'+dateto+'" AND equipment_id like  "%'+equipment_id+'%"'

            cursor.execute(data)
            return cursor.fetchall()
        
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
           
            ZamboangaDB.DATABASE.close()


    @staticmethod
    def select_hauling_id(id):
        """
        This function is for querying with parameters of 
        """

       
        ZamboangaDB.DATABASE._open_connection()

        try:
            data = ' select * from hauling where \
                         id =  "'+id+'"'

            cursor.execute(data)
            return cursor.fetchall()
        
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
           
            ZamboangaDB.DATABASE.close()



    @staticmethod
    def update_hauling(id,trans_date,equipment_id,routes,
                        distance,trackFactor,no_trips,volume,
                        rate,taxRate,amount,vat_output,net_of_vat,user,date_updated):
        """
        This function is to update Hauling with parameters of  ID
        """
        ZamboangaDB.DATABASE._open_connection()
        try:
            data = ('UPDATE hauling SET trans_date=%s,equipment_id=%s,routes=%s,\
                        distance=%s,trackFactor=%s,no_trips=%s,volume=%s,\
                        rate=%s,taxRate=%s,amount=%s,vat_output=%s,net_of_vat=%s,user=%s,date_updated=%s\
                        WHERE id = %s')
            val =(trans_date,equipment_id,routes,
                    distance,trackFactor,no_trips,volume,
                     rate, taxRate,amount,vat_output,net_of_vat,user,
                     date_updated, id)
            cursor.execute(data,val)
           
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
            ZamboangaDB.DATABASE.commit()
            ZamboangaDB.DATABASE.close()


    @staticmethod
    def delete_hauling(id):
        """This function si for deleting Rental with Parametes"""
        ZamboangaDB.DATABASE._open_connection()    

        try:
            data = ('DELETE FROM hauling \
                WHERE id = "'+id+'"')       
                        
            # cursor.execute(data)              
            cursor.execute(data) 
        
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
            ZamboangaDB.DATABASE.commit()
            ZamboangaDB.DATABASE.close()  


    @staticmethod
    def select_hauling_sum_per_equipment(datefrom,dateto,equipment_id):
        """This function is for sum per equipment hauling"""

        ZamboangaDB.DATABASE._open_connection()

        try:
            data = ("SELECT equipment_id,routes,\
                sum(no_trips)  as Trips,\
                sum(volume) as Volume,\
                sum(amount) as Amount,\
                sum(net_of_vat)  as NetAmount\
            from hauling \
            WHERE trans_date BETWEEN '" + datefrom +"'AND '" + dateto +"' AND equipment_id LIKE '%" + equipment_id +"%' \
            GROUP BY equipment_id ,routes \
            ORDER BY equipment_id")
            
            cursor.execute(data)
            return cursor.fetchall()


        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
           
            ZamboangaDB.DATABASE.close()
