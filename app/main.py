from fastapi import Depends, FastAPI, HTTPException

from .db import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/login")
def login(username: str, password: str):
    return {"username": username}


@app.post("/signup", response_model=schemas.User)
def signup(username: str, password: str):
    db_user = crud.get_user_by_email(db, email=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


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