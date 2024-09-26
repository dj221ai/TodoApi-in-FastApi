import models
from fastapi import FastAPI, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from typing import Annotated
from models import Todos
from starlette import status
from pydantic import Field, BaseModel
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

origins = [
    '*',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


# create dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# pydantic
class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description : str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

# @app.get("/", status_code=status.HTTP_200_OK)
# async def read_list(db: db_dependency):
#     return db.query(Todos).all()
@app.get("/", status_code=status.HTTP_200_OK)
async def read_list(db: db_dependency, skip: int = 0, limit: int = 10):
    return db.query(Todos)[skip : skip + limit]
    # return db.query(Todos).all()


@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_model:
        return HTTPException(status_code=404, detail="This id is not Available")
    return todo_model


@app.post("/todo/create", status_code=status.HTTP_201_CREATED)
async def create_task(db:db_dependency, todo_data: TodoRequest):
    todo_model = Todos(**todo_data.model_dump())
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model


@app.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def edit_task(db: db_dependency, todo_data: TodoRequest, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_model:
        return HTTPException(status_code=404, detail="Data not found")
    todo_model.title         = todo_data.title
    todo_model.description   = todo_data.description
    todo_model.priority      = todo_data.priority
    todo_model.complete      = todo_data.complete

    db.add(todo_model)
    db.commit()


@app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(db: db_dependency, todo_data: TodoRequest, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_model:
        return HTTPException(status_code=404, detail="Data Not found")
    db.delete(todo_model)
    db.commit()



    






