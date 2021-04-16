from datetime import date
from fastapi import FastAPI
from models import Todo
from tortoise.contrib.fastapi import register_tortoise
from pydantic import BaseModel

app = FastAPI()


register_tortoise(
    app,
    db_url="sqlite://store.db",
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True,
)


class TodoIn_Pydantic(BaseModel):
    id: int
    todo: str
    due_date: date

    class Config:
        orm_mode = True


class Todo_Pydantic(BaseModel):
    todo: str
    due_date: date

    class Config:
        orm_mode = True


@app.get('/')
async def read_root():
    return {
        "message" : "Hello World",
    }

@app.post('/todo', response_model=Todo_Pydantic)
async def create(todo:TodoIn_Pydantic):
    obj = await Todo.create(**todo.dict(exclude_unset=True))
    return Todo_Pydantic.from_orm(obj)


@app.get('/todo/{id}', response_model=Todo_Pydantic)
async def get(id:int):
    obj = await  Todo.get(id = id)
    print(obj.__dict__)
    return Todo_Pydantic.from_orm(obj)
    