from pydantic import BaseModel, EmailStr
from datetime import datetime
import secrets

class Get_file(BaseModel):
    id: int
    user_id: int
    path: str

    class Config:
        orm_mode = True


class File(BaseModel):
    id: int
    user_id: int
    ivent_id: int
    type: str
    path: str
    datetime: str

    class Config:
        orm_mode = True


class User(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(User):
    pass


class UserToken(BaseModel):
    token: str


class Plot(BaseModel):
    dates: list[datetime] = [
        "2023-02-06 01:17:00",
        "2023-02-06 01:32:00",
        "2023-02-06 01:37:00"
    ]
    markers: dict = {"lat": 37.220,
                     "lon": 37.019,
                     "time": "2023-02-06 01:17:34"}
    lon_limits: tuple[int, int] = [25, 50]
    lat_limits: tuple[int, int] = [25, 50]
    clims: dict = {"ROTI": [-0, 0.5, "TECu/min"]}


# class PlotDT(BaseModel):
#     epcs: dict = {"lat": 37.220,
#                         "lon": 37.019,
#                         "time": datetime(2023, 2, 6, 1, 17, 34)}
#     clims: dict = {"ROTI": [-0,0.5,"TECu/min"]}


