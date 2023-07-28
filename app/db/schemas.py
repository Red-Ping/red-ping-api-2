from pydantic import BaseModel


class PingBase(BaseModel):
    timestamp: str


class PingCreate(PingBase):
    pass


class Ping(PingBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str
    hashed_password: str


'''
class UserCreate(UserBase):
    pass
'''



class User(UserBase):
    id: int
    class Config:
        from_attributes = True

class UserOut(User):
    sent_ping_requests: list[User] = []
    received_ping_requests: list[User] = []
    can_ping: list[User] = []
    can_be_pinged: list[User] = []