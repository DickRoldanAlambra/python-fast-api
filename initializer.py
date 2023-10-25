from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Column, DateTime, Integer, String, Boolean, ForeignKey
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

connection_string = f"mssql+pyodbc://{db_username}:{db_password}@{db_server}/{db_database}?driver=SQL Server"
# engine = create_engine(connection_string)
# Debugging
engine = create_engine(connection_string, echo=True)
#This resolves issues with bulk inserts or operations:
connection = engine.raw_connection()
connection.cursor().fast_executemany = True
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()