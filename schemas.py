from pydantic import BaseModel,EmailStr
from datetime import datetime
import secrets

class File(BaseModel):
    id: int
    user_id: int
    ivent_id: int
    type: str
    path: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    #files: list[File] = []

    class Config:
        orm_mode = True


#class Ivent(BaseModel):
#    token: str
#    datetime_start: datetime
#    datetime_end: datetime

 #   class Config:
#        orm_mode = True