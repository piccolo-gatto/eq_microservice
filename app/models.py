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
    path = Column(Text)
    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime)

    user = relationship("User", back_populates="files")
