from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ..db import crud
from ..db.schemas import UserOut
from ..auth.access import verify_user
from ..db.database import SessionLocal

router = APIRouter()

def get_db():
    with SessionLocal() as db:
        return db
    
db = get_db()

#Accept a ping request
@router.post("/ping_accept")
def ping_accept(user_email: str, user: Annotated[UserOut, Depends(verify_user)]):
    
    #Checks if the user exists
    invalid_user = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid User",
    )

    #Check if the user exists
    request_user = crud.get_user_by_email(db, user_email)
    if not request_user:
        raise invalid_user
    
    #Same session user
    user = crud.get_user_by_email(db, user.email)

    #Checks if the user has a ping request from the other user
    if user_email not in user.received_ping_requests:
        raise invalid_user
    
    #Accepts the ping request
    crud.accept_ping_request(db, user, request_user)

    #It succeeded
    return HTTPException(status_code=status.HTTP_200_OK)

#Decline a ping request
@router.post("/ping_decline")
def ping_decline(user_email: str, user: Annotated[UserOut, Depends(verify_user)]):
    
    #Checks if the user exists
    invalid_user = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid User",
    )

    #Check if the user exists
    request_user = crud.get_user_by_email(db, user_email)
    if not request_user:
        raise invalid_user
    
    #Same session user
    user = crud.get_user_by_email(db, user.email)

    #Checks if the user has a ping request from the other user
    if user_email not in user.received_ping_requests:
        raise invalid_user
    
    #Declines the ping request
    crud.decline_ping_request(db, user, request_user)

    #It succeeded
    return HTTPException(status_code=status.HTTP_200_OK)
