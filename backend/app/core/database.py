from sqlalchemy import create_engine # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore
import psycopg2 # type: ignore
import time

from app.core.config import settings

# Create database engine
engine = create_engine(settings.DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)


def wait_for_db():
    """Wait for the database to be ready"""
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(settings.DATABASE_URL)
            conn.close()
            return
        except psycopg2.OperationalError:
            retries -= 1
            print(f"Database not ready, waiting... ({retries} attempts left)")
            time.sleep(2)
    
    print("Could not connect to database after multiple attempts")
    raise Exception("Database connection failed")