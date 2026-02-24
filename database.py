#this file is responsible for creating the database connection and session. It uses SQLAlchemy to create an engine and a sessionmaker, which are used to interact with the database. The database URL is loaded from an environment variable using the dotenv library. The base class is also defined here, which is used to create the ORM models in the models.py file.

from sqlalchemy import create_engine;
from sqlalchemy.orm import sessionmaker, declarative_base;
from dotenv import load_dotenv;
import os;
load_dotenv()
DATABASE_URL = os.getenv("DATABASE")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()

