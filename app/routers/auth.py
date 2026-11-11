from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models import User
from app import models,schemas,utils
from app.oauth2 import create_access_token

router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.get("/login")
def login():
    return {"message":"Login succesfullly"}



@router.post("/logins")
def logins(
    user_cerdentials:OAuth2PasswordRequestForm =Depends(),
    db:Session=Depends(get_db)
):
    user=db.query(User).filter(User.email==user_cerdentials.username).first()
    
    if user is None:
        raise HTTPException(status_code=403,detail="invalid cerdentials")
        

    if not utils.verify(user_cerdentials.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="invalid cerdebtails"
        )
    access_token=create_access_token({"user_id":user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    

