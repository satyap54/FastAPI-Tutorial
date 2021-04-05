from fastapi import FastAPI
from typing import Optional


app = FastAPI()


@app.get('/')
async def hello_world():
    return {
        "message" : "Hello World",
    }


@app.get('/component/{component_id}') # path parameters
async def get_component(component_id : int):
    return{
        "component_id" : component_id,
    }


@app.get('/component') # query parameters
async def read_componenet(number : int, text : str):
    return{
        "query" : number + " " + text,
    }