from sqlalchemy.orm import Session
from argon2 import PasswordHasher

from . import models, schemas

ph = PasswordHasher()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()
    

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

#Creates a user hashing the function
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.email, hashed_password=ph.hash(user.password))
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