from sqlalchemy.orm import Session
from argon2 import PasswordHasher, exceptions

from . import models, schemas

ph = PasswordHasher()

def get_user_by_email(db: Session, email: str) -> schemas.UserOut:
    return db.query(models.User).filter(models.User.email == email).first()

#Sets the password hash for a user
def set_password_hash_for_user(db: Session, email: str,  password: str):
    user = get_user_by_email(db, email)
    user.hashed_password = ph.hash(password)
    db.commit()
    return user

#Todo move this to auth
#Check username and password
def authenticate_user(db: Session, email: str, password: str):
    
    #Techincally this style of programming could leak the username via timing attacks
    user = get_user_by_email(db, email=email)
    if not user:
        return False
    try:
        ph.verify(user.hashed_password, password)
    except exceptions.InvalidHash:
        return False
    if ph.check_needs_rehash(user.hashed_password):
        set_password_hash_for_user(db, user.email, password)
    return user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

#Creates a user hashing the function
def create_user(db: Session, email: str, password: str):
    db_user = models.User(email=email, hashed_password=ph.hash(password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#Adds a ping request to a user and the user that sent the request
def add_ping_request(db: Session, user: schemas.UserOut, request_user: schemas.UserOut):
    user.sent_ping_requests.append(request_user)
    #request_user.received_ping_requests.append(user)
    db.commit()

#Gets the ping requests for a user with the email
def get_ping_request(db: Session, email: str):
    user = get_user_by_email(db, email)
    user_emails = [user.email for user in user.received_ping_requests]
    return user_emails

#Accepts a ping request
def accept_ping_request(db: Session, user: schemas.UserOut, request_user: schemas.UserOut):
    user.can_ping.append(request_user)
    #request_user.can_be_pinged.append(user)
    db.commit()

#Declines a ping request
def decline_ping_request(db: Session, user: schemas.UserOut, request_user: schemas.UserOut):
    user.received_ping_requests.remove(request_user)
    #request_user.sent_ping_requests.remove(user)
    db.commit()

#Creates a ping
def create_ping(db: Session, ping: schemas.PingCreate, sender_id: int, receiver_id: int):
    db_ping = models.Ping(**ping.model_dump(), sender_id=sender_id, receiver_id=receiver_id)
    db.add(db_ping)
    db.commit()
    db.refresh(db_ping)
    return db_ping