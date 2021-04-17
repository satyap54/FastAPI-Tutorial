import schemas
import jwt
from models import User
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from tortoise.contrib.fastapi import register_tortoise
from passlib.hash import bcrypt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
JWT_SECRET = "808a34c7d52df4f04d41c76d92b49aa161803aaa3b61a2d2cd4a9ae2bda04b44"


register_tortoise(
    app, 
    db_url="sqlite://store.db",
    modules = {
        'models' : ['models'],
    },
    generate_schemas = True,
    add_exception_handlers = True
)

async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user

@app.post('/auth/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    user_obj = schemas.UserPydantic.from_orm(user)
    token = jwt.encode(user_obj.dict(), JWT_SECRET)
    return{
        "access_token": token,
        "token_type": "bearer",
    }

@app.post('/register')
async def creater_user(user: schemas.UserInPydantic):
    user_obj = await User.create(username=user.username, password_hash=bcrypt.hash(user.password))
    await user_obj.save()
    obj = schemas.UserPydantic.from_orm(user_obj)
    return obj

async def get_current_user(token: str= Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await User.get(id=payload.get('id'))
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    obj = schemas.UserPydantic.from_orm(user)
    return obj

@app.get('/users/me', response_model=schemas.UserPydantic)
async def get_user(user: schemas.UserPydantic = Depends(get_current_user)):
    return user
