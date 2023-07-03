from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from fastapi import HTTPException
import os
import secrets
from datetime import datetime
from pathlib import Path
from loguru import logger
from sqlalchemy import and_

from . import models, schemas

STORAGE_PATH = Path('./app/files')
TOKEN_LENGTH = 16

logger.add("./logs/info.log", retention="1 week")

def get_user_by_email(db: Session, email: str):
    try:
        db_user = db.query(models.User).filter(models.User.email == email).first()
    except:
        logger.error("Error get user data by email")
        raise HTTPException(status_code=500, detail="Error get user data by email")
    return db_user


def get_ivent_token_by_datetime(db: Session, datetime_start: datetime, datetime_end: datetime):
    try:
        ivent = db.query(models.Ivent).filter(
            and_(models.Ivent.datetime_start == datetime_start, models.Ivent.datetime_end == datetime_end)).first()
        if ivent == None:
            token = generate_token()
            logger.info(f"{token} Create new ivent")
            create_ivent(db=db, datetime_start=datetime_start, datetime_end=datetime_end, token=token)
        else:
            token = ivent.token
            logger.info(f"{token} Token for ivent is getting")
    except:
        logger.error("Error get ivent token by datetime")
        raise HTTPException(status_code=500, detail="Error get ivent token by datetime")
    return token


def get_ivent_by_token(db: Session, token: str):
    try:
        db_ivent = db.query(models.Ivent).filter(models.Ivent.token == token).first()
    except:
        logger.error("Error get ivent data by token")
        raise HTTPException(status_code=500, detail="Error get ivent data by token")
    return db_ivent


def generate_token():
    logger.info("Generating a token")
    token = secrets.token_hex(TOKEN_LENGTH)
    return token

def create_user(db: Session, user: schemas.UserToken):
    token = generate_token()
    db_user = models.User(email=user.email, token=token)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"New DB user {db_user.token} was successfully created")
    return db_user

def upload_file(db: Session, user_id: int, ivent_id: int, path: str, type: str, datetime: datetime):
    db_file = models.Uploaded_file(user_id=user_id, ivent_id=ivent_id, path=path, type=type, datetime=datetime)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    logger.info(f"New DB file {db_file.id} was successfully created")
    return db_file


def create_ivent(db: Session, datetime_start: datetime, datetime_end: datetime, token: str):
    db_ivent = models.Ivent(datetime_start=datetime_start, datetime_end=datetime_end, token=token)
    db.add(db_ivent)
    db.commit()
    db.refresh(db_ivent)
    logger.info(f"New DB ivent {db_ivent.token} was successfully created")
    return db_ivent


def make_processing_dir(token: str):
    pth = STORAGE_PATH / str(token)
    if not pth.exists():
        os.makedirs(pth)
    else:
        logger.info("It's directory is making")
    return pth


def get_id_by_token(db: Session, token: str):
    try:
        user = db.query(models.User).filter(models.User.token == token).first()
    except:
        logger.error("Error receiving user data by token")
        raise HTTPException(status_code=500, detail="Error receiving user data by token")
    return user.id

def get_last_uploaded_files(db: Session, user_id: int):
    return db.query(models.Uploaded_file).filter(models.Uploaded_file.user_id == user_id).order_by(models.Uploaded_file.datetime.desc()).limit(10).all()

def get_last_uploaded_files(db: Session, user_id: int):
    user_token = db.query(models.User).filter(models.User.id == user_id).first().token
    try:
        logger.info(f'Getting files for user {user_token}')
    except:
        logger.error(f'Error receiving data for user {user_token}')
        raise HTTPException(status_code=500, detail=f'Error receiving data for user {user_id}')
    return db.query(models.Uploaded_file).filter(models.Uploaded_file.user_id == user_id).order_by(models.Uploaded_file.datetime.desc()).limit(10).all()

def get_files_by_date(db: Session, user_id: int, date_start: datetime, date_end: datetime):
    user_token = db.query(models.User).filter(models.User.id == user_id).first().token
    try:
        logger.info(f'Getting files for user {user_token} and date {date_start}')
    except:
        logger.error(f'Error receiving data for user {user_token} and date {date_start}')

        
def get_files_by_date(db: Session, user_id: int, date_start: datetime, date_end: datetime):
    return db.query(models.Uploaded_file).filter(
        models.Uploaded_file.user_id == user_id,
        models.Uploaded_file.datetime >= date_start,
        models.Uploaded_file.datetime <= date_end
    ).all()

def make_result_dir(path: str, type: str = ''):
    file_path, file = path.split('/')
    file_name = file.split('.')[0]
    result_path = file_path + '/result/'
    if not Path(result_path).exists():
        os.makedirs(result_path)
    else:
        logger.info("It's directory is making")
    result_path = result_path + file_name + f'_{type}.png'
    return result_path


def upload_result_file(db: Session, file_id: int, path: str, type: str):
    db_file = models.Result_file(file_id=file_id, path=path, type=type)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    logger.info(f"New DB result file {db_file.id} was successfully created")
    return db_file
