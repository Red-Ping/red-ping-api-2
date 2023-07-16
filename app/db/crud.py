from sqlalchemy.orm import Session
from argon2 import PasswordHasher, exceptions

from . import models, schemas

ph = PasswordHasher()

def get_user_by_email(db: Session, email: str) -> schemas.UserCreate:
    return db.query(models.User).filter(models.User.email == email).first()

#Sets the password hash for a user
def set_password_hash_for_user(db: Session, email: str,  password: str):
    user = get_user_by_email(db, email)
    user.hashed_password = ph.hash(password)
    db.commit()
    return user

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

#Creates a ping
def create_ping(db: Session, ping: schemas.PingCreate, sender_id: int, receiver_id: int):
    db_ping = models.Ping(**ping.dict(), sender_id=sender_id, receiver_id=receiver_id)
    db.add(db_ping)
    db.commit()
    db.refresh(db_ping)
    return db_ping