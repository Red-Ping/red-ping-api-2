import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ..db import crud
from ..db.schemas import User
from ..auth.access import verify_user
from ..db.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db = next(get_db())

#Requesting to ping a user
@router.post("/ping_request")
def post_ping_request(user_email: str, user: Annotated[User, Depends(verify_user)]):
    
    #Not sure if we can have more descriptive errors without leaking information
    invalid_user = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid User",
    )

    #Check if the user exists
    request_user = crud.get_user_by_email(db, user.email)
    if not request_user:
        raise invalid_user
    
    #Check if the user has already requested to ping the other user
    
    

#Get the current ping requests
@router.get("/ping_request")
def get_ping_request():
    return {"status": "healthy"}
