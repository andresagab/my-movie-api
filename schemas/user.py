from pydantic import BaseModel

# define schema of users
class User(BaseModel):
    email:str
    password: str