
from fastapi import APIRouter, Depends
from app.schemas import StudentCreate
from app.dependencies import get_db
from sqlalchemy.orm import Session
from app import models,schemas
from app import utils



router=APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/")
def get_user():
    return {"message":"All User"}

@router.post("/student")
def create_student(student:StudentCreate,db:Session=Depends(get_db)):

    new_student=models.Student(
        name=student.name,
        age=student.age
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

@router.get("/students")
def get_student(db:Session=Depends(get_db)):
    student=db.query(models.Student).all()

    return student

@router.get("/student/{id}")
def get_single_student(id:int,db:Session=Depends(get_db)):
    students=(db.query(models.Student)
            .filter(models.Student.id==id)
            .first()
)
    return students


@router.put("/students/{id}")
def update_student(
    id:int,student:StudentCreate,
    db:Session=Depends(get_db)
):
    
    existing=(
        db.query(models.Student)
        .filter(models.Student.id==id)
        .first()
    )

    if existing is None:
        return {"Message":"Student not found"}
    
    existing.name=student.name
    existing.age=student.age

    db.commit()
    db.refresh(existing)
    return existing



@router.delete("/student/{id}")
def delete_student(id:int,db:Session=Depends(get_db)):

    students=(
        db.query(models.Student)
        .filter(models.Student.id==id)
        .first()
    )
    
    if students is None:
        return {"message":"Student not found"}
    
    db.delete(students)
    db.commit()

    return {"message":"Delete successfully"}


@router.post("/hashing")
def create_password(user:schemas.UserCreate,db:Session=Depends(get_db)):

    hashed_password=utils.hash(user.password)

    new_user=models.User(
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user