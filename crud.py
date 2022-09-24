from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status

not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="not found"
)


def get_todo(id: int, db: Session) -> schemas.TodoOut:
    todo = db.query(models.Todo).filter(models.Todo.id == id).first()
    if todo is None:
        raise not_found_exception
    return todo


def get_todos(db: Session) -> list[schemas.TodoOut]:
    todos = db.query(models.Todo).all()
    return todos


def create_todo(todo: schemas.TodoIn, db: Session):
    new_todo = models.Todo(**todo.dict())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return todo


def delete_todo(id: int, db: Session):
    todo = db.query(models.Todo).filter(models.Todo.id == id)
    if todo.first() is None:
        raise not_found_exception
    todo.delete()
    db.commit()
    return {"message": "deleted"}


def update_todo(id: int, todo_in: schemas.TodoIn, db: Session):
    todo = db.query(models.Todo).filter(models.Todo.id == id)
    if todo.first() is None:
        raise not_found_exception
    todo.update(todo_in.dict())
    db.commit()
    return todo_in
