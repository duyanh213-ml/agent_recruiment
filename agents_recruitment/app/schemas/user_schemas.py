from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    username: str
    hash_password: str
    role: str
    is_active: bool
    created_date: datetime
    updated_date: datetime


class UserCreate(BaseModel):
    name: str
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
