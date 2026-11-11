#jwt token
from datetime import datetime,timedelta,timezone

from jose import jwt
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError,jwt
from sqlalchemy.orm import Session

from .models import User
from .dependencies import get_db


#-----------------
#jwt configuration
#-----------------

SECRET_KEY="your-super-secret-key"   #jwt configuration  change this prpduction
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30


oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")  #oauth2 schema and url path

#------------------
#create access token
#-------------------
def create_access_token(data:dict):
    to_encode=data.copy()

    expire=datetime.now(timezone.utc)+timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp":expire})

    encode_jwt=jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encode_jwt

# -----------------------
# Verify Current User
# ----------------------

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not found cerdentials",
        headers={"WWW-Authenticate":"Bearer"}
    )

    try:
        payload=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=ALGORITHM
        )
        user_id=payload.get("user_id")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception
    
    user=(
        db.query(User).filter(User.id==user_id)
        .first()
    )
    if user is None:
        raise credentials_exception
    
    return user