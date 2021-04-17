from pydantic import BaseModel


class UserPydantic(BaseModel):
    id: int
    username: str
    password_hash: str

    class Config:
        orm_mode = True


class UserInPydantic(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True