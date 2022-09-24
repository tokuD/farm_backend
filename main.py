from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import engine, get_db
import models, schemas, crud
from sqlalchemy.orm import Session

# modelsを介したBaseじゃないと動かない
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/todo", response_model=list[schemas.TodoOut])
async def get_todos(db: Session = Depends(get_db)):
    return crud.get_todos(db)

@app.get("/api/todo/{id}", response_model=schemas.TodoOut)
async def get_todo_by_id(id: int, db: Session = Depends(get_db)):
    return crud.get_todo(id, db)

@app.post("/api/todo", response_model=schemas.TodoOut)
async def post_todo(todo: schemas.TodoIn, db: Session = Depends(get_db)):
    return crud.create_todo(todo, db)

@app.put("/api/todo/{id}", response_model=schemas.TodoOut)
async def put_todo(id: int, todo: schemas.TodoIn, db: Session = Depends(get_db)):
    return crud.update_todo(id, todo, db)

@app.delete("/api/todo/{id}")
async def delete_todo(id: int, db: Session = Depends(get_db)):
    return crud.delete_todo(id, db)