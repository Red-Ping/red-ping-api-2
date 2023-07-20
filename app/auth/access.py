from datetime import datetime, timedelta
from jose import JWTError, jwt

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..db import crud, models, schemas
from ..db.database import SessionLocal

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db = next(get_db())


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
          raise HTTPException(status.HTTP_401_UNAUTHORIZED, 
                              "Incorrect username or password",
                              {"WWW-Authenticate": "Bearer"},
                            )
    #auth(user)
    return {"cookie": "cookies need to be setup"}

@router.post("/signup")
def signup(email: str, password: str):
    user = crud.get_user_by_email(db, email=email)
    if user:
        raise HTTPException(status_code=409, detail="User already registered")
    user = crud.create_user(db, email, password)
    #jwt = auth(user)
    return {"cookie": "cookies need to be setup"}