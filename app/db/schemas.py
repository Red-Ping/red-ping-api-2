from pydantic import BaseModel


class PingBase(BaseModel):
    timestamp: str


class PingCreate(PingBase):
    pass


class Ping(PingBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    sender_id: int
    receiver_id: int
    sender: list[Ping] = []

    class Config:
        orm_mode = True
