from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Todos
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=3, max_length=100)  
    priority: int = Field(gt=0, lt=6)
    completed: bool = False
    # def __repr__(self):

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    todos = db.query(Todos).all()
    return todos

@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo is not None:
        return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@router.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoRequest, db: db_dependency):
    new_todo_model = Todos(**todo.model_dump())
    db.add(new_todo_model)
    db.commit()
    # db.refresh(new_todo_model)
    # return new_todo_model

@router.put("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(todo: TodoRequest, db: db_dependency, todo_id: int = Path(gt=0)):
    todo_to_update = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_to_update is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_data = todo.model_dump(exclude_unset=True)
    for key, value in todo_data.items():
        setattr(todo_to_update, key, value)
    db.commit()
    return todo_to_update

@router.put("/todos/2/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(todo: TodoRequest, db: db_dependency, todo_id: int = Path(gt=0)):
    todo_to_update = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_to_update is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo_to_update.title = todo.title
    todo_to_update.description = todo.description
    todo_to_update.priority = todo.priority
    todo_to_update.completed = todo.completed
    
    db.add(todo_to_update)
    db.commit()

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_to_delete = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_to_delete is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo_to_delete)
    # db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
