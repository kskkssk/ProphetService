from pydantic import BaseModel, EmailStr
from typing import List


class UserBase(BaseModel):
    username: str
    password: str
    email: EmailStr
    first_name: str
    last_name: str

    class Config:
        orm_mode = True
        from_attributes = True


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True
        from_attributes = True


class UserSignin(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True
        from_attributes = True

class UserResponse(UserBase):
    transaction_list: List[dict]

    class Config:
        orm_mode = True
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True
        from_attributes = True
