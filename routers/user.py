from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from jwt_manager import create_token

# define user router
userRouter = APIRouter()

# define schema of users
class User(BaseModel):
    email:str
    password: str

# post /login => to authenticate user
@userRouter.post('/login', tags = ['auth'])
def login(user: User):
    if user.email == "admin@admin.com" and user.password == "admin":
        # call to create token sending user convert to dict
        token: str = create_token(user.dict())
        # return JSON response with status code and token
        return JSONResponse(status_code = 200, content = token)
    return user