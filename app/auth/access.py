from datetime import datetime, timedelta
from jose import JWTError, jwt

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..db import crud
from ..db.schemas import User
from ..db.database import SessionLocal

from .schemas import TokenData

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#Constants need to probably be changed
# openssl rand -hex 32
SECRET_KEY: str
ALGORITHM = "HS512"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db = next(get_db())

def setup_secret_key(secret_key):
    global SECRET_KEY
    if not secret_key:
        raise ValueError("Secret key cannot be empty")
    SECRET_KEY = secret_key

def verify_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload =  jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        exp = payload.get("exp")
        if email is None:
            raise credentials_exception
        if exp is None:
            raise credentials_exception
        if datetime.utcnow() > datetime.fromtimestamp(exp):
            raise credentials_exception

        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, token_data.email)
    if user is None:
        raise credentials_exception
    return user

#Authenticates a user
def auth(user):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return access_token

#Creates an jwt access token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = crud.authenticate_user(db, form_data.username, form_data.password)

    if not user:
          raise HTTPException(status.HTTP_401_UNAUTHORIZED, 
                              "Incorrect username or password",
                              {"WWW-Authenticate": "Bearer"})
    access_token = auth(user)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/signup")
def signup(email: str, password: str):
    user = crud.get_user_by_email(db, email=email)
    if user:
        raise HTTPException(status.HTTP_409_CONFLICT, 
                            "User already registered")
    user = crud.create_user(db, email, password)
    access_token = auth(user)
    return {"access_token": access_token, "token_type": "bearer"}


#This requires auth
@router.get("/get_email")
def get_email(user: Annotated[User, Depends(verify_user)]):
    return {"email": user.email}
