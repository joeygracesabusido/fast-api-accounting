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




    @staticmethod
    def insertEquipment(equipmentID, equipmentDesc, rentalRate, remarks):
        """This is to insert to database rental to equipment_rental Table"""

        try:
            # Create a cursor object
            
            TviDB.DATABASE._open_connection()
            cursor = TviDB.DATABASE.cursor()
            # Use parameterized queries to prevent SQL injection attacks
            data = (
                "INSERT INTO equipment (equipmentID, equipmentDesc, rentalRate, remarks) "
                "VALUES (%s, %s, %s, %s)"
            )
            val = (equipmentID, equipmentDesc, rentalRate, remarks)

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
    def selectEquipment(id):
        """
        This function is for querying all equipment
        """

        # try:
        #     # Open the database connection and create a cursor
        #     with TviDB.DATABASE:
        #         cursor = TviDB.DATABASE.cursor()

        #         # Use a parameterized query to prevent SQL injection attacks
        #         cursor.execute('SELECT * FROM equipment WHERE id like  "%'+id+'%" ')

        #         # Return the results of the query
        #         equipment = cursor.fetchone()

        #         # Check if no equipment was found
        #         if equipment is None:
        #             return "No equipment found with ID {}".format(id)

        #         # Return the equipment data
        #         return equipment
        # except Exception as ex:
        #     print("Error", f"Error occurred: {str(ex)}")


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
    def update_equipment(id, equipmentId, equipmentDesc,rentalRate, remarks):
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
                    SET equipmentId = %s, equipmentDesc = %s, rentalRate = %s,remarks = %s
                    WHERE id = %s
                '''
                cursor.execute(update_query, (equipmentId, equipmentDesc,rentalRate, remarks, id))
                TviDB.DATABASE.commit()
                # TviDB.DATABASE.close()
            except Exception as ex:
                print("Error", f"Error due to :{str(ex)}")


#===========================================This is for Rental Transaction ===============================
    @staticmethod
    # def insertRental(transDate, equipmentId, totalHours, rentalRate,
    #                   taxRate, vat_output, driverOperator,user,date_credited):
    #     """This is to insert to database rentalTransaction Table"""
    #     TviDB.DATABASE._open_connection()
    #     with TviDB.DATABASE.cursor() as cursor:
    #         try:
    #         # Use the insert method to insert the data into the database
    #             cursor.execute(
    #                 "INSERT INTO rentalTransaction",
    #                 {
    #                     "transDate": transDate,
    #                     "equipmentId": equipmentId,
    #                     "totalHours": totalHours,
    #                     "rentalRate": rentalRate,
    #                     "taxRate": taxRate,
    #                     "vat_output": vat_output,
    #                     "driverOperator": driverOperator,
    #                     "user": user,
    #                     "date_credited": date_credited,
    #                 }
    #             )
    #             TviDB.DATABASE.commit()
            
    #         except Exception as ex:
    #         # Roll back any changes to the database if an error occurs
    #             TviDB.DATABASE.rollback()
    #             print("Error: ", str(ex))
    def insertRental(transDate, equipmentId, totalHours, rentalRate, taxRate, vat_output, driverOperator, user, date_credited):
        """This is to insert to database rentalTransaction Table"""

        # Constants for the column names and data types
        TRANS_DATE = "transDate"
        EQUIPMENT_ID = "equipmentId"
        TOTAL_HOURS = "totalHours"
        RENTAL_RATE = "rentalRate"
        TAX_RATE = "taxRate"
        VAT_OUTPUT = "vat_output"
        DRIVER_OPERATOR = "driverOperator"
        USER = "user"
        DATE_CREDITED = "date_credited"

        # Construct the parameterized query
        query = f"INSERT INTO rentalTransaction ({TRANS_DATE}, {EQUIPMENT_ID}, {TOTAL_HOURS}, {RENTAL_RATE}, {TAX_RATE}, {VAT_OUTPUT}, {DRIVER_OPERATOR}, {USER}, {DATE_CREDITED}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        # Create a data dictionary for the values to be inserted
        data = {
            TRANS_DATE: transDate,
            EQUIPMENT_ID: equipmentId,
            TOTAL_HOURS: totalHours,
            RENTAL_RATE: rentalRate,
            TAX_RATE: taxRate,
            VAT_OUTPUT: vat_output,
            DRIVER_OPERATOR: driverOperator,
            USER: user,
            DATE_CREDITED: date_credited,
        }

        # Add additional error checking here, if necessary

        # Open the database connection
        TviDB.DATABASE._open_connection()

        # Use a try-except block to handle errors gracefully
        try:
            with TviDB.DATABASE.cursor() as cursor:
                # Execute the parameterized query
                cursor.execute(query, data.values())
            # Commit the transaction
            TviDB.DATABASE.commit()
        except Exception as ex:
            # Roll back the transaction and close the connection
            TviDB.DATABASE.rollback()
            print("Error: ", str(ex))
        finally:
            # Close the connection
            TviDB.DATABASE.close()
      










