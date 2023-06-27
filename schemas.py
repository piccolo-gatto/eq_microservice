from pydantic import BaseModel,EmailStr
from datetime import datetime
import secrets

class FileBase(BaseModel):
    pass

class FileCreate(FileBase):
    pass


class File(FileBase):
    id: int
    user_id: int
    path: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    files: list[File] = []

    class Config:
        orm_mode = True


class IventBase(BaseModel):
    start_datetime: datetime
    end_datetime: datetime

class IventCreate(IventBase):
    pass


class Ivent(IventBase):
    token: str

    class Config:
        orm_mode = True