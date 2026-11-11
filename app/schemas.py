from pydantic import BaseModel,EmailStr

class StudentCreate(BaseModel):
    name:str
    age:int

class UserCreate(BaseModel):
    email:EmailStr
    password:str