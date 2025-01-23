from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    name: str
    username: str
    hash_password: str
    role: str
    is_active: bool
    created_date: datetime = datetime.now()
    updated_date: datetime = datetime.now()


class UserCreate(BaseModel):
    name: str
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
