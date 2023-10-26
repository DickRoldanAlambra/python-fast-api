from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, URL, Column, DateTime, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from decimal import Decimal
from pydantic import BaseModel
from fastapi import FastAPI,HTTPException,APIRouter
from typing import List

app = FastAPI()

load_dotenv()

# Get database credentials from environment variables
db_server = os.getenv("DB_SERVER")
db_database = os.getenv("DB_DATABASE")
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")

connection_string = f"DRIVER=SQL Server;SERVER={db_server};DATABASE={db_database};UID={db_username};PWD={db_password}"
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})

# engine = create_engine(connection_string)
# Debugging
engine = create_engine(connection_url, echo=True)
#This resolves issues with bulk inserts or operations:
connection = engine.raw_connection()
connection.cursor().fast_executemany = True
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()