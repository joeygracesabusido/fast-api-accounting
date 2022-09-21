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


import mysql.connector
import logging as logger
class Database:
    __instance = None
    def __init__(self):
        if self.__instance is None or self.__instance.is_connected() == False:
            self.__instance = mysql.connector.connect(
              host="192.46.225.247",
                user="joeysabusido",
                password="Genesis@11",
                database="ldglobal",
            )
            self.__instance.autocommit = False
    def query(self, query, autoCommit=None, fetch="ALL"):
        try:
            cursor = self.__instance.cursor()
            result = cursor.execute(query)
            if autoCommit is not None:
                self.__instance.commit()
                operation = True if cursor.lastrowid == 0 else {"id": cursor.lastrowid}
                return {"result": operation}
            fields = [field_md[0] for field_md in cursor.description]
            if fetch != "SINGLE":
                result = [dict(zip(fields, row)) for row in cursor.fetchall()]
                return {"result": result}
            else:
                result = [dict(zip(fields, row)) for row in cursor.fetchone()]
                return {"result": result}
        except Exception as e:
            return {"result": None, "error": e, "query": query}
            logger.error(e)
        finally:
            if self.__instance.is_connected():
                logger.info("Mantendo conexão.")
#                 # self.__instance.cursor.close()
#                 # self.__instance.close()
#                 # logger.debug("Removendo instancia da Database... OK")