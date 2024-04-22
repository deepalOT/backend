from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
# username = 'sa'
# password = 'orange505'
# server = 'server'
# database = 'Orange_Hrms_Odoo'

import urllib
params = urllib.parse.quote_plus("DRIVER={SQL Server};"
                                 "SERVER=server;"
                                 "DATABASE=Orange_Hrms_Odoo;"
                                 "UID=sa;"
                                 "PWD=orange505")

engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params), connect_args={"check_same_thread": False})

SessionLocal  =  sessionmaker(autocommit=False, autoflush=True, bind=engine)

# Test the connection
# try:
#     with engine.connect() as connection:
#         print("Connected successfully!")
# except Exception as e:
#     print("Connection failed:", e)


def get_session():
    with Session(engine.connect()) as session:
        try:
            yield session
        except:
            session.rollback()
            raise
        finally:
            session.close()

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    except:
        db.rollback()
    finally:
        db.close_all()