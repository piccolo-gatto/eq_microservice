from pydantic import BaseModel,EmailStr
from datetime import datetime
import secrets


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    #files: list[File] = []

    class Config:
        orm_mode = True