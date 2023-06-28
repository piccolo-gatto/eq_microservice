from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
import os
import secrets
import shutil
from datetime import datetime
from pathlib import Path

from . import models, schemas

from sqlalchemy.orm import Session

STORAGE_PATH = Path('/eq_data')
CLEAN_AFTER_SECONDS = 24 * 3600 * 30
TOKEN_LENGTH = 16

def get_user_by_email(db: Session, email: str):
    try:
        return db.query(models.User).filter(models.User.email == email).first()
    except:
        pass
        #return logger.error("Error receiving user data by email")
    

def get_ivent_by_token(db: Session, token: str):
    ivent = db.query(models.Ivent).filter(models.Ivent.token == token).first()
    return user

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def upload_file(db: Session, user_id: int, ivent_id: int, path: str, type: str, datetime: datetime):
    db_file = models.Uploaded_file(user_id=user_id, ivent_id=ivent_id, path=path, type=type, datetime=datetime)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def create_ivent(db: Session, datetime_start: datetime, datetime_end: datetime, token: str):
    db_ivent = models.Ivent(datetime_start=datetime_start, datetime_end=datetime_start, token=token)
    db.add(db_ivent)
    db.commit()
    db.refresh(db_ivent)
    return db_ivent

def make_processing_dir(token: str):
    pth = STORAGE_PATH / token
    if not pth.exists():
        os.makedirs(pth)
    else:
        raise ProcessingDirExists
    return pth
