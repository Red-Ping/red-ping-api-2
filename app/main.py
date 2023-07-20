from fastapi import Depends, FastAPI, HTTPException, status

from typing import Annotated

from .db import crud, models, schemas
from .db.database import SessionLocal, engine

from .auth.access import router as access_router

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(access_router)


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
