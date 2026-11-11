from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from app.routers import user
from app.routers import post
from app.routers import auth
from .database import engine
from .import models



models.Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)

# class UserCreate(BaseModel):
#     name:str=Field(min_length=2,max_length=10)
#     age:int=Field(ge=13,le=100)
#     goal:str

class UserCreate(BaseModel):
    name:str
    age:int
    email:str
    password:int

class UserResponce(BaseModel):
    id:int
    name:str
    age:int
    email:str


@app.post("/users_create",response_model=UserResponce)
def user_create(user:UserCreate):

    save_user={
        "id":1,
        "name":user.name,
        "email":user.email,
        "age":user.age,
        "password_hash":"example_hash"

    }
    return save_user


@app.post("/users")
def user_creates(user:UserCreate):
    return{
        "Message":"user Created Sucessfully",
        "user":user
    }




# @app.post("/users")
# def get_user(user:UserCreate):
#     return{
#         "message":"User Create Sucessfully",
#         "user":user

#     }



products=[
    {"id":1,"name":"vinoth","age":20},
    {"id":2,"name":"Priya","age":19},
    {"id":3,"name":"Jashvika","age":23}
]

@app.get("/")
def get_main():
    return {"Sucessfully Login"}

@app.get("/Product")
def get_product():
    return products

@app.get("/product/{products_id}")
def get_product_id(products_id:int):

    for product in products:
        if product["id"]==products_id:
            return product

    raise HTTPException(
        status_code=404,
        detail="Product not Found"
    )

@app.post("/product")
def create_product(product:dict):
    products.append(product)
    return{
        "message":"Product Created",
        "Product" :product
    }

