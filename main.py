from fastapi import FastAPI, Depends, HTTPException
from schemas import Todo as Todoschema, TodoCreate
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
from models import Todo
Base.metadata.create_all(bind=engine) #This is for creating the database tables based on the models defined in the models.py file. It uses the metadata from the Base class to create the tables in the database if they do not already exist.

app = FastAPI()

#Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db #Yield is the return variable for the dependency, it is used to return the database session to the endpoint function. The try block is used to ensure that the database session is closed after the endpoint function is executed, even if an error occurs.
    finally:
        db.close()

# POST - create ToDo
#This is called routing, it is used as a @app.post()
@app.post("/todos", response_model=Todoschema)
def create(todo: TodoCreate, db:Session = Depends(get_db)):
    db_todo = Todo(**todo.dict())
    db.add(db_todo) #this is for created table item, it adds the item to the database session, but it is not yet committed to the database. The commit() method is called later to save the changes to the database.
    db.commit()  # Save changes to the database
    db.refresh(db_todo) #This is for refreshing the id from the Todo model. 
    return db_todo # this is for returning the created items.

#Get - read ToDo (All Todo)
@app.get("/todos", response_model=list[Todoschema])
def read_todos(db:Session = Depends(get_db)):
    return db.query(Todo).all() #This is for returning all the items in the database. The query() method is used to query the database for the Todo model, and the all() method is used to return all the items in the database as a list.

#Get - read ToDo (Single Todo)
@app.get("/todos/{todo_id}", response_model=Todoschema)
def read_todo(todo_id: int, db:Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

#PUT -> Update Todo
@app.put("/todos/{todo_id}", response_model=Todoschema)
def update_todo(todo_id: int, updated_todo: TodoCreate, db:Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in updated_todo.dict().items():
        setattr(todo, key, value)
    db.commit()
    db.refresh(todo)
    return todo

#DELETE - delete todo
@app.delete("/todo/{todo_id}")
def delete_todo(todo_id: int, db:Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}
    