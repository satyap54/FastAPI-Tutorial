from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel


app = FastAPI()


class Package(BaseModel):
    name : str
    number : str
    description : Optional[str] = None


class PackageIn(BaseModel):
    id : int
    name : str
    number : str
    description : Optional[str] = None


@app.get("/")
async def index():
    return{
        "message" : "Index",
    }

@app.post("/package/{id}", response_model=Package, response_model_exclude_unset=True)
async def make_package(id: int, package: PackageIn):
    return package