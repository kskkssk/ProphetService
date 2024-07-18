from pydantic import BaseModel, EmailStr
from typing import List


class UserBase(BaseModel):
    id: int
    username: str
    password: str
    email: EmailStr
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class UserSignin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    transaction_list: List[dict]

    class Config:
        from_attributes = True
