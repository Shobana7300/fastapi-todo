#This is the models.py file which defines the database model for the Todo application. It uses SQLAlchemy to define a Todo class that represents a table in the database. The table has columns for id, title, description, and completed status.

from sqlalchemy import Column, Integer, String, Boolean
from database import Base;   

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)