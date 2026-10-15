from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker

#Find the backend directory
BASE_DIR = Path(__file__).resolve().parents[2]

#store database inside the backend directory
DATABASE_URL = f"sqlite:///{BASE_DIR/'opspilot.db'}"

#create the database engine
engine = create_engine(
    DATABASE_URL,
    echo=False,
)

@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

#Base class for database models
class Base(DeclarativeBase):
    pass        

#Create a session factory for database interactions
SessionLocal = sessionmaker(
     autoflush=False, 
     bind=engine,
     expire_on_commit=False,
)