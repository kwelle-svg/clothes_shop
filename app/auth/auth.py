from datetime import datetime, timedelta, timezone
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGHORITM = os.getenv("ALGHORITM")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGHORITM)


from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.settings import db_dependency
from app.models.users_model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")

# async def get_current_user(token: str = Depends(oauth2_scheme),
#                            access_token: str = Cookie(None)):
#     auth_token = token or access_token
#     if not auth_token:
#         raise HTTPException(status_code=401)
    
#     if auth_token.startswith("Bearer "):
#         auth_token = auth_token.replace("Bearer ", "")
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGHORITM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise HTTPException(status_code=401)
#         return email
#     except:
#         raise HTTPException(status_code=401, detail="Could not validate user.")
    
async def get_current_user(db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGHORITM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401)
        user = db.query(User).filter(User.email==email).first()
        if user is None:
            raise HTTPException(status_code=401)
        return user
    except:
        raise HTTPException(status_code=401, detail="Could not validate user.") 