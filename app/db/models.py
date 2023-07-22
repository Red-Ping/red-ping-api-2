from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship

from .database import Base


# Many to many relationship between users
user_requests_association = Table(
    "user_requests_association",
    Base.metadata,
    Column("user_sent_request_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("user_recv_request_id", Integer, ForeignKey("users.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    #Users that this user has sent ping requests to

    sent_ping_requests = relationship(
        "User",
        secondary="user_requests_association",
        primaryjoin=id == user_requests_association.c.user_recv_request_id,
        secondaryjoin=id == user_requests_association.c.user_sent_request_id,
        backref="received_ping_requests",
    )

    

class Ping(Base):
    __tablename__ = "pings"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime)
