from fastapi import FastAPI, HTTPException
from typing import Optional, List
from models import Todo

app = FastAPI()


'''
    CRUD functionality implementation
'''

# Dummy db since am not using a real database
store_todo = []


@app.get('/')
async def home():
    return{
        "message" : "Hello World",
    }


@app.post('/todo/')
async def create_todo(todo: Todo):
    store_todo.append(todo)
    return todo


@app.get('/todo/', response_model= List[Todo])
async def get_all_todos():
    return store_todo


@app.get('/todo/{id}')
async def get_todo(id : int):
    try:
        return store_todo[id]
    except:
        raise HTTPException(status_code=404, detail="Todo not found")


@app.put('/todo/{id}')
async def update_todo(id: int, todo : Todo):
    try:
        store_todo[id] = todo
    except:
        raise HTTPException(status_code=404, detail="Todo not found")


@app.delete('/todo/{id}')
async def delete_todo(id: int):
    try:
        obj = store_todo[id]
        store_todo.pop(id)
        return obj
    except:
        raise HTTPException(status_code=404, detail="Todo not found")