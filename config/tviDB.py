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

        # try: 
        #     cursor.execute(
        #         """CREATE TABLE IF NOT EXISTS rentalTransaction (id INT AUTO_INCREMENT PRIMARY KEY, 
        #                     transDate date,
        #                     equipmentId VARCHAR (100) NOT NULL, 
        #                     totalHours DECIMAL(9,2),
        #                     rentalRate DECIMAL(9,2),
        #                     totalAmount DECIMAL(9,2) GENERATED ALWAYS AS (totalHours*rentalRate) STORED,
        #                     taxRate DECIMAL(3,2),
        #                     vat_output DECIMAL(9,2),
        #                     net_of_vat DECIMAL(9,2) GENERATED ALWAYS AS (totalAmount-vat_output) STORED,
        #                     driverOperator VARCHAR (100) NOT NULL, 
        #                     user VARCHAR(100),
        #                     date_updated date,
        #                     date_credited DATETIME NOT NULL) """)
                    
        # except Exception as ex:
        #     print("Error", f"Error due to :{str(ex)}")

        # finally:
        #     TviDB.DATABASE.commit()
        #     TviDB.DATABASE.close()

        # Add a column to the table after another column
        # try:
        #     table_name = 'rentalTransaction'
        #     after_column = 'driverOperator'
        #     new_column_name = 'owner'
        #     new_column_type = 'VARCHAR(50)'
        #     alter_table_query = f'ALTER TABLE {table_name} ADD COLUMN {new_column_name} {new_column_type} AFTER {after_column}'
        #     cursor.execute(alter_table_query)
        # except Exception as ex:
        #     print("Error", f"Error due to :{str(ex)}")

        # finally:
        #     TviDB.DATABASE.commit()
        #     TviDB.DATABASE.close()



    @staticmethod
    def insertEquipment(equipmentID, equipmentDesc, rentalRate, remarks,owner):
        """This is to insert to database rental to equipment_rental Table"""

        try:
            # Create a cursor object
            
            TviDB.DATABASE._open_connection()
            cursor = TviDB.DATABASE.cursor()
            # Use parameterized queries to prevent SQL injection attacks
            data = (
                "INSERT INTO equipment (equipmentID, equipmentDesc, rentalRate, remarks,owner) "
                "VALUES (%s, %s, %s, %s, %s)"
            )
            val = (equipmentID, equipmentDesc, rentalRate, remarks, owner)

            # Execute the query and save the changes to the database
            cursor.execute(data, val)
            TviDB.DATABASE.commit()

        except Exception as ex:
            # Roll back any changes to the database if an error occurs
            TviDB.DATABASE.rollback()
            print("Error: ", str(ex))

        finally:
            # Close the cursor and connection to the database
            cursor.close()
            TviDB.DATABASE.close()


    @staticmethod
    def selectAllEquipment():
        """
        This function is for querying all equipment
        """

        # try:
        #     # Open the database connection and create a cursor
        #     with TviDB.DATABASE:
        #         cursor = TviDB.DATABASE.cursor()

        #         # Use a parameterized query to prevent SQL injection attacks
        #         cursor.execute("SELECT * FROM equipment")

        #         # Return the results of the query
        #         return cursor.fetchall()
        # except Exception as ex:
        #     print("Error", f"Error occurred: {str(ex)}")


        TviDB.DATABASE._open_connection()
        cursor = TviDB.DATABASE.cursor()
        try:
            data = 'SELECT * FROM equipment '

            cursor.execute(data)
            return cursor.fetchall()
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
            # Database.DATABASE.commit()
            TviDB.DATABASE.close()

    @staticmethod
    def selectEquipmentIDAutocomplete(equipmentId):
        """
        This function is for querying all equipment
        """

       
        TviDB.DATABASE._open_connection()
        try:
            with TviDB.DATABASE.cursor() as cursor:
                # Use parameterized query to prevent SQL injection attacks
                query = 'SELECT * FROM equipment WHERE equipmentId like %s'
                cursor.execute(query, (f'%{equipmentId}%',))
                rows = cursor.fetchall()
                if not rows:
                    return []
                return rows
        except Exception as ex:
            # Raise the exception to be handled at a higher level
            raise ex
        finally:
            # Close the connection, regardless of whether an exception occurred
            TviDB.DATABASE.close()

    @staticmethod
    def selectEquipmentID(equipmentId):
        """
        This function is for querying equipment with parameters
        """

       
        TviDB.DATABASE._open_connection()
        try:
            with TviDB.DATABASE.cursor() as cursor:
                # Use parameterized query to prevent SQL injection attacks
                query = 'SELECT * FROM equipment WHERE equipmentId like %s'
                cursor.execute(query, (f'%{equipmentId}%',))
                rows = cursor.fetchall()
                if not rows:
                    return []
                return rows
        except Exception as ex:
            # Raise the exception to be handled at a higher level
            raise ex
        finally:
            # Close the connection, regardless of whether an exception occurred
            TviDB.DATABASE.close()



    @staticmethod
    def selectEquipment(id):
        """
        This function is for querying all equipment
        """

      


        TviDB.DATABASE._open_connection()
        cursor = TviDB.DATABASE.cursor()
        try:
            data = 'SELECT * FROM equipment WHERE id like  "%'+id+'%" '

            cursor.execute(data)
            return cursor.fetchall()
        except Exception as ex:
            print("Error", f"Error due to :{str(ex)}")
        finally:
            # Database.DATABASE.commit()
            TviDB.DATABASE.close()

    @staticmethod
    def update_equipment(id, equipmentId, equipmentDesc,rentalRate, remarks, owner):
        """
        This function is to update Equipment with parameters of ID
        """
        # Use the `with` statement to handle opening and closing the database connection
        # with TviDB.DATABASE:
        TviDB.DATABASE._open_connection()
        cursor = TviDB.DATABASE.cursor()
        with TviDB.DATABASE:
            try:
                # Use a parameterized query to prevent SQL injection attacks
                update_query = '''
                    UPDATE equipment
                    SET equipmentId = %s, equipmentDesc = %s, rentalRate = %s,remarks = %s, owner = %s
                    WHERE id = %s
                '''
                cursor.execute(update_query, (equipmentId, equipmentDesc,rentalRate, remarks,owner, id))
                TviDB.DATABASE.commit()
                # TviDB.DATABASE.close()
            except Exception as ex:
                print("Error", f"Error due to :{str(ex)}")


#===========================================This is for Rental Transaction ===============================
    @staticmethod
    def insertRental(transDate, equipmentId, totalHours, rentalRate, taxRate,
                                 vat_output, driverOperator, user, owner, date_credited):
        """This is to insert to database rentalTransaction Table"""

      
        # Open the database connection
        TviDB.DATABASE._open_connection()

        try:
            with TviDB.DATABASE.cursor() as cursor:


                data = (
                        "INSERT INTO rentalTransaction (transDate, equipmentId, totalHours, rentalRate, \
                            taxRate, vat_output, driverOperator, user,owner,date_credited ) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    )
                val = (transDate, equipmentId, totalHours, rentalRate, taxRate,
                                 vat_output, driverOperator, user,owner, date_credited)

                # Execute the query and save the changes to the database
                cursor.execute(data, val)
                TviDB.DATABASE.commit()

        except Exception as ex:
            # Roll back any changes to the database if an error occurs
            TviDB.DATABASE.rollback()
            print("Error: ", str(ex))

        finally:
            # Close the cursor and connection to the database
            cursor.close()
            TviDB.DATABASE.close()

    @staticmethod
    def selectAllRental(datefrom,dateto,equipmentID,onwer):
        """
        This function is for querying all Rental Transactions
        """

        TviDB.DATABASE._open_connection()
        SELECT_QUERY = 'SELECT * FROM rentalTransaction \
                        WHERE transDate BETWEEN "'+datefrom+'" AND "'+dateto+'" \
                        AND equipmentID like  "%'+equipmentID+'%" \
                            AND owner like "%'+onwer+'%"'

        with TviDB.DATABASE as cnx:
            with cnx.cursor() as cursor:
                try:
                    cursor.execute(SELECT_QUERY)
                    return cursor.fetchall()
                except mysql.connector.Error as ex:
                    print(f"Error due to: {str(ex)}")

    @staticmethod
    def selectRentalperID(id):
        """
        This function is for querying all Rental Transactions with ID
        """

        TviDB.DATABASE._open_connection()
        SELECT_QUERY = 'SELECT * FROM rentalTransaction \
                        WHERE id like  "%'+id+'%" \
                            '

        with TviDB.DATABASE as cnx:
            with cnx.cursor() as cursor:
                try:
                    cursor.execute(SELECT_QUERY)
                    return cursor.fetchall()
                except mysql.connector.Error as ex:
                    print(f"Error due to: {str(ex)}")

    @staticmethod
    def delete_rental_trans(id):
        """This function is for deleting Rental Trans with parameters"""
        DELETE_QUERY = 'DELETE FROM rentalTransaction WHERE id = %s'

        TviDB.DATABASE._open_connection()
        with TviDB.DATABASE as cnx:
            with cnx.cursor() as cursor:
                try:
                    cursor.execute(DELETE_QUERY, (id,))
                except mysql.connector.Error as ex:
                    print(f"Error due to: {str(ex)}")
                else:
                    cnx.commit()


    @staticmethod
    def update_rentalTrans(id, transDate, equipmentId, totalHours, rentalRate, taxRate,
                                 vat_output, driverOperator, user, owner, date_updated):
        """
        This function is to update Rental Transaction with parameters of ID
        """
        # Use the `with` statement to handle opening and closing the database connection
        # with TviDB.DATABASE:
        TviDB.DATABASE._open_connection()
        cursor = TviDB.DATABASE.cursor()
        with TviDB.DATABASE:
            try:
                # Use a parameterized query to prevent SQL injection attacks
                update_query = '''
                    UPDATE rentalTransaction
                    SET transDate = %s, equipmentId = %s, totalHours = %s,rentalRate = %s, taxRate = %s,
                    vat_output = %s, driverOperator = %s, user = %s, owner = %s, date_updated = %s
                    WHERE id = %s
                '''
                cursor.execute(update_query, (transDate, equipmentId, 
                                            totalHours,rentalRate, taxRate,
                                            vat_output,driverOperator,user,
                                             owner,date_updated, id))
                TviDB.DATABASE.commit()
                # TviDB.DATABASE.close()
            except Exception as ex:
                print("Error", f"Error due to :{str(ex)}")
      










