from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String)
    token = Column(String)

    files = relationship("Uploaded_file", back_populates="user")


class Uploaded_file(Base):
    __tablename__ = "uploaded_files"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ivent_id = Column(Integer, ForeignKey("ivents.id"))
    type = Column(String)
    path = Column(String)
    datetime = Column(String)

    user = relationship("User", back_populates="files")
    ivent = relationship("Ivent", back_populates="files")
    res_files = relationship("Result_file", back_populates="up_files")

class Ivent(Base):
    __tablename__ = "ivents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    datetime_start = Column(String)
    datetime_end = Column(String)
    token = Column(String)

    files = relationship("Uploaded_file", back_populates="ivent")


class Result_file(Base):
    __tablename__ = "result_files"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("uploaded_files.id"))
    type = Column(String)
    path = Column(String)

    up_files = relationship("Uploaded_file", back_populates="res_files")