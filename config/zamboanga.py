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

        try: 
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS routes (id INT AUTO_INCREMENT PRIMARY KEY, 
                            routes_name VARCHAR(100), 
                            distance DECIMAL(9,2),
                            UNIQUE (routes_name))""")
                    
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")

        finally:
            ZamboangaDB.DATABASE.commit()
            ZamboangaDB.DATABASE.close()

        # try: 
        #     cursor.execute(
        #         """CREATE TABLE IF NOT EXISTS hauling (id INT AUTO_INCREMENT PRIMARY KEY, 
        #                     trans_date date,
        #                     routes VARCHAR(100),
        #                     distance DECIMAL(9,2), 
        #                     trackFactor DECIMAL(9,2),
        #                     no_trips DECIMAL(9,2),
        #                     rate DECIMAL(9,2),
        #                     taxRate DECIMAL(3,2),
        #                     vat_output DECIMAL(9,2),
        #                     net_of_vat DECIMAL(9,2) 
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
