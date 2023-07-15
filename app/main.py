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
    return {"email": email}


@app.post("/signup", response_model=schemas.User)
def signup(email: str, password: str):
    db_user = crud.get_user_by_email(db, email=email)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    user = crud.create_user(db=db, user=schemas.UserCreate(email=email, password=password))
    return user


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
