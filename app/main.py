from fastapi import Depends, FastAPI, HTTPException

from .db import crud, models, schemas
from .db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db = next(get_db())

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/login")
def login(email: str, password: str):
    user = crud.authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    #auth(user)
    return {"cookie": "cookies need to be setup"}

@app.post("/signup")
def signup(email: str, password: str):
    user = crud.get_user_by_email(db, email=email)
    if user:
        raise HTTPException(status_code=409, detail="User already registered")
    user = crud.create_user(db, email, password)
    #auth(user)
    return {"cookie": "cookies need to be setup"}


#Requesting to ping a user
@app.post("/ping_request")
def post_ping_request():
    return {"status": "healthy"}

#Get the current ping requests
@app.get("/ping_request")
def get_ping_request():
    return {"status": "healthy"}

#Sends a ping to a user
@app.post("/ping_send")
def post_ping_send():
    return {"status": "healthy"}

#Get the current pings
@app.get("/ping_send")
def get_ping_send():
    return {"status": "healthy"}
