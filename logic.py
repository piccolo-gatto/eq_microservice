from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from . import models, schemas

from sqlalchemy.orm import Session

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def upload_file(db: Session, user_id: int, path: str):
    db_file = models.Uploaded_file(user_id=user_id, path=path)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def create_ivent(db: Session, datetime: schemas.IventCreate, token: str):
    db_ivent = models.Ivent(start_datetime=datetime.start_datetime, end_datetime=datetime.end_datetime, token=token)
    db.add(db_ivent)
    db.commit()
    db.refresh(db_ivent)
    return db_ivent