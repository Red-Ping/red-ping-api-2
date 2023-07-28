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

#Requesting to ping a user
@router.post("/ping_request")
def post_ping_request(user_email: str, user: Annotated[UserOut, Depends(verify_user)]):
    
    #Not sure if we can have more descriptive errors without leaking information
    invalid_user = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid User",
    )

    #Check if the user exists
    request_user = crud.get_user_by_email(db, user_email)
    if not request_user:
        print("User does not exist")
        raise invalid_user

    #Different session user
    user = crud.get_user_by_email(db, user.email)

    #Check if we are the user
    if request_user.email == user.email:
        print("User is the same")
        raise invalid_user
    
    #Check if the user has already requested to ping the other user
    if user_email in request_user.sent_ping_requests:
        print("User has already requested to ping the other user")
        raise invalid_user

    #Now we send the ping request
    crud.add_ping_request(db, user, request_user)

    #It succeeded   
    return HTTPException(status_code=status.HTTP_200_OK)


#Get the current ping requests
@router.get("/ping_request")
def get_ping_request(user: Annotated[UserOut, Depends(verify_user)]):
    return crud.get_ping_request(db, user.email)
