from fastapi import APIRouter, HTTPException, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.settings import db_dependency, templates
from app.auth.auth import get_current_user, create_access_token
from app.auth.hashing import Hasher
from app.models.users_model import User

router = APIRouter(
    tags=["Users"],
    prefix="/user"
    )

@router.get("/")
async def get(request: Request):
    return templates.TemplateResponse(name="auth.html", request=request)

@router.get("/me")
async def read_users_me(current_user: str = Depends(get_current_user)):
    return {"user": current_user, "message": "message"}

@router.post("/create")
async def create(db: db_dependency, name=Form(), email=Form(), password=Form()):
    hashed_password = Hasher.get_password_hash(password=password)
    new_user = User(name=name, email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

def get_user(email: str, db: Session):
    query = select(User).where(User.email==email)
    result = db.execute(query)
    return result.scalar_one_or_none()

# @router.post("/token")
# async def login(db: db_dependency, email=Form(), password=Form()):
#     user = get_user(email=email, db=db)
#     if not user:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     if not Hasher.verify_password(password, user.hashed_password):
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
    
#     access_token = create_access_token(data={"sub": user.email})
#     res = RedirectResponse(url="/user/me", status_code=status.HTTP_303_SEE_OTHER)
#     res.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
#     # return res
#     return {"access_token": access_token, "token_type": "bearer"} 

@router.post("/token")
async def login(db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(email=form_data.username, db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    if not Hasher.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user.email})
    return{"access_token": access_token, "token_type": "bearer"}