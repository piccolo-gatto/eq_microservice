from pydantic import BaseModel,EmailStr
from datetime import datetime


class FileBase(BaseModel):
    path: str
    start_datetime: datetime
    end_datetime: datetime


class FileCreate(FileBase):
    pass


class File(FileBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class User(BaseModel):
    email: EmailStr


class UserCreate(User):
    pass


class UserToken(BaseModel):
    token: str
