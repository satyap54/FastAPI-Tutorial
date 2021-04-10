from fastapi import FastAPI, HTTPException
from models import Todo, TodoIn_Pydantic, Todo_Pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from pydantic import BaseModel

app = FastAPI()


register_tortoise(
    app,
    db_url="sqlite://store.db",
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.get('/')
async def read_root():
    return {
        "message" : "Hello World",
    }

@app.post('/todo', response_model=Todo_Pydantic)
async def create(todo:TodoIn_Pydantic):
    obj = await Todo.create(**todo.dict(exclude_unset=True))
    return await Todo_Pydantic.from_tortoise_orm(obj)


@app.get('/todo/{id}', response_model=Todo_Pydantic, responses={404: {"model" : HTTPNotFoundError}})
async def get(id:int):
    return await Todo_Pydantic.from_queryset_single(Todo.get(idid))
    