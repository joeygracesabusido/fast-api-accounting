from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import *

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

sql_database_url="mysql+pymysql://host:192.46.225.247,user:joeysabusido,password:Genesis@11/ldgsurigao"

engine=create_engine(sql_database_url)

# meta = MetaData()
# con=engine.connect()
sessionLocal=sessionmaker(autocommit=False,bind=engine)

Base=declarative_base()