#this is 

from pydantic import BaseModel

#Validate the table items from models.py 
class TodoBase(BaseModel):
    title: str
    description: str| None = None
    completed: bool = False

#create a new item in the table
class TodoCreate(TodoBase):
    pass

#this is for the response model, it will include the id of the item
#orm_mode is set to True to allow the response model to work with the ORM models and convert the JSON response to the correct format
class Todo(TodoBase):
    id :int
    model_config = {
        "from_attributes": True
    }

        