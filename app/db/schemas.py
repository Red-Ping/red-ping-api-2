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


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    #sender_id: int
    #receiver_id: int
    #sender: list[Ping] = []

    class Config:
        from_attributes = True
