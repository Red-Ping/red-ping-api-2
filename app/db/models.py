from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship
from .database import Base

class UserRequestsAssociation(Base):
    __tablename__ = "user_requests_association"

    user_sent_request_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    user_recv_request_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    def __repr__(self):
        return (
            f"UserRequestsAssociation(user_sent_request_id={self.user_sent_request_id}, "
            f"user_recv_request_id={self.user_recv_request_id})"
        )

class UserCanPingAssociation(Base):
    __tablename__ = "user_can_ping_association"

    user_can_ping_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    user_recv_ping_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    def __repr__(self):
        return (
            f"UserCanPingAssociation(user_can_ping_id={self.user_can_ping_id}, "
            f"user_recv_ping_id={self.user_recv_ping_id})"
        )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    #Users that this user has sent ping requests to (Many to Many)
    sent_ping_requests = relationship(
        "User",
        secondary="user_requests_association",
        primaryjoin=id == UserRequestsAssociation.user_recv_request_id,
        secondaryjoin=id == UserRequestsAssociation.user_sent_request_id,
        backref="received_ping_requests",
    )
    #received_ping_requests is a ref to sent_ping_requests

    #Users that this user can ping (Many to Many)
    can_ping = relationship(
        "User",
        secondary="user_can_ping_association",
        primaryjoin=id == UserCanPingAssociation.user_recv_ping_id,
        secondaryjoin=id == UserCanPingAssociation.user_can_ping_id,
        backref="can_be_pinged",
    )  
    #can_be_pinged is a ref to can_ping

    def __repr__(self):
        return f"User(id={self.id}, email={self.email}), sent_ping_requests={self.sent_ping_requests}, received_ping_requests={self.received_ping_requests})"

class Ping(Base):
    __tablename__ = "pings"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime)

    def __repr__(self):
        return f"Ping(id={self.id}, sender_id={self.sender_id}, receiver_id={self.receiver_id}, timestamp={self.timestamp})"
